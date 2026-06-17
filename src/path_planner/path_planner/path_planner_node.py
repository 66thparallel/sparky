import rclpy
from rclpy.node import Node

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')

        self.path_pub = self.create_publisher(Path, '/path', 10)

        self.timer = self.create_timer(1.0, self.publish_path)

        self.get_logger().info("Path Planner Node started")

    def publish_path(self):
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()

        # simple square loop
        waypoints = [
            (0.0, 0.0),
            (2.0, 0.0),
            (2.0, 2.0),
            (0.0, 2.0),
            (0.0, 0.0),
        ]

        for x, y in waypoints:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = path.header.stamp

            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0

            pose.pose.orientation.w = 1.0  # no rotation for now

            path.poses.append(pose)

        self.path_pub.publish(path)


def main(args=None):
    rclpy.init(args=args)
    node = PathPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()