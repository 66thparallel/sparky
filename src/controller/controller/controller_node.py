import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.loop)  # 10 Hz

        self.get_logger().info("Controller node started")

    def loop(self):
        msg = Twist()

        # basic forward motion
        msg.linear.x = 1.0
        msg.angular.z = 0.0

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()