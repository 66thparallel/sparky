import rclpy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from nav_msgs.msg import Path
import rclpy


class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')

        self.declare_parameter('frame_id', 'map')
        self.declare_parameter(
            'waypoints',
            [0.0, 0.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 0.0, 0.0],
        )

        self.path_pub = self.create_publisher(Path, '/path', 10)
        self.metrics_pub = self.create_publisher(DiagnosticArray, '/metrics/planner', 10)
        self.frame_id = self.get_parameter('frame_id').value
        self.waypoints = self._load_waypoints()
        self.previous_publish_time = None

        self.timer = self.create_timer(1.0, self.publish_path)

        self.get_logger().info(
            f"Path Planner Node started with {len(self.waypoints)} waypoint(s)"
        )

    def _load_waypoints(self):
        flat_waypoints = list(self.get_parameter('waypoints').value)

        if len(flat_waypoints) < 4:
            raise ValueError(
                "The 'waypoints' parameter must contain at least two x/y pairs."
            )

        if len(flat_waypoints) % 2 != 0:
            raise ValueError(
                "The 'waypoints' parameter must contain an even number of values."
            )

        return [
            (float(flat_waypoints[index]), float(flat_waypoints[index + 1]))
            for index in range(0, len(flat_waypoints), 2)
        ]

    def publish_path(self):
        publish_time = self.get_clock().now()
        path = Path()
        path.header.frame_id = self.frame_id
        path.header.stamp = publish_time.to_msg()

        for x, y in self.waypoints:
            pose = PoseStamped()
            pose.header.frame_id = self.frame_id
            pose.header.stamp = path.header.stamp

            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0

            pose.pose.orientation.w = 1.0  # no rotation for now

            path.poses.append(pose)

        self.path_pub.publish(path)
        self.publish_metrics(publish_time)

    def publish_metrics(self, publish_time):
        publish_interval_ms = 0.0
        loop_rate_hz = 0.0

        if self.previous_publish_time is not None:
            publish_interval_ms = (
                (publish_time - self.previous_publish_time).nanoseconds * 1e-6
            )
            if publish_interval_ms > 0.0:
                loop_rate_hz = 1000.0 / publish_interval_ms

        self.previous_publish_time = publish_time

        metrics_msg = DiagnosticArray()
        metrics_msg.header.stamp = publish_time.to_msg()

        status = DiagnosticStatus()
        status.name = 'planner_metrics'
        status.message = 'planner telemetry'
        status.values = [
            KeyValue(key='frame_id', value=str(self.frame_id)),
            KeyValue(key='waypoint_count', value=str(len(self.waypoints))),
            KeyValue(key='publish_interval_ms', value=str(publish_interval_ms)),
            KeyValue(key='loop_rate_hz', value=str(loop_rate_hz)),
        ]

        metrics_msg.status = [status]
        self.metrics_pub.publish(metrics_msg)


def main(args=None):
    rclpy.init(args=args)
    node = PathPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()