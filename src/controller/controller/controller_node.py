import math
import time

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path, Odometry
import rclpy
from rclpy.node import Node


class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        # tunable parameters
        self.lookahead_dist = 0.8
        self.k_steer = 1.5
        self.max_speed = 1.0

        # ros i/o
        self.pub = self.create_publisher(Twist, '/cmd_drive', 10)
        self.metrics_pub = self.create_publisher(DiagnosticArray, '/metrics/controller', 10)

        self.create_subscription(Path, '/path', self.path_callback, 10)
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.timer = self.create_timer(0.1, self.update)

        # state
        self.path = None

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.odom_ready = False
        self.previous_steering_command = None

        self.get_logger().info("Pure Pursuit Controller started")

    # callbacks
    def path_callback(self, msg):
        self.path = msg

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.yaw = math.atan2(siny, cosy)

        self.odom_ready = True

    # core control loop
    def update(self):
        if not self.odom_ready or self.path is None:
            return

        control_start = time.perf_counter()
        lookahead_point = self.find_lookahead_point()
        if lookahead_point is None:
            return

        cmd, heading_error, curvature = self.compute_control(lookahead_point)
        cross_track_error = self.compute_cross_track_error()
        steering_oscillation = self.compute_steering_oscillation(cmd.angular.z)
        control_latency_ms = (time.perf_counter() - control_start) * 1000.0

        self.pub.publish(cmd)
        self.publish_metrics(
            lookahead_point,
            heading_error,
            curvature,
            cmd,
            cross_track_error,
            steering_oscillation,
            control_latency_ms,
        )

    # pure pursuit
    def find_lookahead_point(self):
        for pose_stamped in self.path.poses:
            dx = pose_stamped.pose.position.x - self.x
            dy = pose_stamped.pose.position.y - self.y

            dist = math.sqrt(dx * dx + dy * dy)

            if dist >= self.lookahead_dist:
                return pose_stamped.pose.position

        return None

    def compute_control(self, target):
        dx = target.x - self.x
        dy = target.y - self.y

        # angle to target in world frame
        target_angle = math.atan2(dy, dx)

        # heading error
        alpha = target_angle - self.yaw
        alpha = math.atan2(math.sin(alpha), math.cos(alpha))

        # calculate curvature to waypoint
        curvature = 2.0 * math.sin(alpha) / max(self.lookahead_dist, 0.01)

        cmd = Twist()
        cmd.linear.x = self.max_speed * (1.0 - min(abs(alpha), 1.0))
        cmd.angular.z = self.k_steer * curvature

        return cmd, alpha, curvature

    def compute_cross_track_error(self):
        if self.path is None or not self.path.poses:
            return 0.0

        return min(
            math.hypot(
                pose_stamped.pose.position.x - self.x,
                pose_stamped.pose.position.y - self.y,
            )
            for pose_stamped in self.path.poses
        )

    def compute_steering_oscillation(self, steering_command):
        if self.previous_steering_command is None:
            self.previous_steering_command = steering_command
            return 0.0

        oscillation = abs(steering_command - self.previous_steering_command)
        self.previous_steering_command = steering_command
        return oscillation

    def publish_metrics(
        self,
        target,
        heading_error,
        curvature,
        cmd,
        cross_track_error,
        steering_oscillation,
        control_latency_ms,
    ):
        metrics_msg = DiagnosticArray()
        metrics_msg.header.stamp = self.get_clock().now().to_msg()

        status = DiagnosticStatus()
        status.name = 'controller_metrics'
        status.message = 'controller telemetry'
        status.values = [
            KeyValue(key='cross_track_error', value=str(cross_track_error)),
            KeyValue(key='heading_error', value=str(heading_error)),
            KeyValue(key='steering_command', value=str(cmd.angular.z)),
            KeyValue(key='steering_oscillation', value=str(steering_oscillation)),
            KeyValue(key='commanded_speed', value=str(cmd.linear.x)),
            KeyValue(key='curvature', value=str(curvature)),
            KeyValue(key='control_latency_ms', value=str(control_latency_ms)),
            KeyValue(key='lookahead_distance', value=str(self.lookahead_dist)),
            KeyValue(key='target_x', value=str(target.x)),
            KeyValue(key='target_y', value=str(target.y)),
            KeyValue(key='path_pose_count', value=str(len(self.path.poses))),
        ]

        metrics_msg.status = [status]
        self.metrics_pub.publish(metrics_msg)


def main():
    rclpy.init()
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()