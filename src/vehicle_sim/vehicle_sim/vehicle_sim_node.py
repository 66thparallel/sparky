import rclpy
from rclpy.node import Node

class VehicleSimNode(Node):
    def __init__(self):
        super().__init__('vehicle_sim_node')
        self.get_logger().info('Vehicle simulator node started!')

def main(args=None):
    rclpy.init(args=args)
    node = VehicleSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()