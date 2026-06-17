import rclpy
from rclpy.node import Node

import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path, Odometry


class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        # tunable parameters
        self.lookahead_dist = 0.8
        self.k_steer = 1.5
        self.max_speed = 1.0

        # ros i/o
        self.pub = self.create_publisher(Twist, '/cmd_drive', 10)

        self.create_subscription(Path, '/path', self.path_callback, 10)
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.timer = self.create_timer(0.1, self.update)

        # state
        self.path = None

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.odom_ready = False

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

        lookahead_point = self.find_lookahead_point()
        if lookahead_point is None:
            return

        cmd = self.compute_control(lookahead_point)
        self.pub.publish(cmd)

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

        return cmd


def main():
    rclpy.init()
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()