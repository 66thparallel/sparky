import math
import rclpy
import tf_transformations
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class VehicleState:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.velocity = 0.0

class VehicleSimNode(Node):
    def __init__(self):
        super().__init__('vehicle_sim_node')
        self.get_logger().info('Vehicle simulator node started!')
        self.dt = 0.02
        self.wheelbase = 0.30
        # create state variables
        self.state = VehicleState()
        self.commanded_speed = 0.0
        self.commanded_steering = 0.0
        # subscribe to commands
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_drive',
            self.cmd_callback,
            10
        )
        # create the 50 Hz timer (every 20 ms run an update)
        self.timer = self.create_timer(
            0.02,
            self.update
        )
        # create odometry publisher
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

    def update(self):
        """ This is the vehicle simulation. """
        # set speed
        self.state.velocity = self.commanded_speed
        # update position
        self.state.x += (
            self.state.velocity *
            math.cos(self.state.yaw) *
            self.dt
        )
        self.state.y += (
            self.state.velocity *
            math.sin(self.state.yaw) *
            self.dt
        )
        # update heading
        self.state.yaw += (
            self.state.velocity /
            self.wheelbase *
            math.tan(self.commanded_steering) *
            self.dt
        )
        # publish odometry
        odom = Odometry()
        # timestamp of when this measurement was produced
        odom.header.stamp = (
            self.get_clock().now().to_msg()
        )
        # position (x, y) is expressed in the map coordinate frame
        odom.header.frame_id = "map"
        # velocity is describing the vehicle body (base_link)
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = self.state.x
        odom.pose.pose.position.y = self.state.y
        odom.twist.twist.linear.x = (
            self.state.velocity
        )
        # set the orientation
        q = tf_transformations.quaternion_from_euler(
            0.0, 0.0, self.state.yaw
        )

        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        # publish the message
        self.odom_pub.publish(odom)




    
    def cmd_callback(self, msg):
        """ Create the callback. Whenever a controller publishes a command, these values update. """
        self.commanded_speed = msg.linear.x
        self.commanded_steering = max(
            -0.6,
            min(0.6, msg.angular.z)
        )


def main(args=None):
    rclpy.init(args=args)
    node = VehicleSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()