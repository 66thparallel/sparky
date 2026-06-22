import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from tf2_ros import StaticTransformBroadcaster
from tf_transformations import quaternion_from_euler
from nav_msgs.msg import Odometry


class VehicleState:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.velocity = 0.0


class VehicleSimNode(Node):
    def __init__(self):
        super().__init__("vehicle_sim_node")
        self.get_logger().info("Vehicle simulator node started!")
        self.wheelbase = 0.30

        # create state variables
        self.state = VehicleState()
        self.commanded_speed = 0.0
        self.commanded_steering = 0.0

        # subscribe to commands
        self.cmd_sub = self.create_subscription(
            Twist, "/cmd_drive", self.cmd_callback, 10
        )

        # update the simulator at 50 Hz
        self.timer = self.create_timer(0.02, self.update)

        # create odometry publisher
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)

        # initialize TF broadcaster
        self.static_tf_broadcaster = StaticTransformBroadcaster(self)
        self.tf_broadcaster = TransformBroadcaster(self)

        # time tracking (shared by both odom + TF)
        self.last_time = self.get_clock().now()

        # static transform
        map_tf = TransformStamped()

        map_tf.header.stamp = self.get_clock().now().to_msg()
        map_tf.header.frame_id = "map"
        map_tf.child_frame_id = "odom"

        map_tf.transform.translation.x = 0.0
        map_tf.transform.translation.y = 0.0
        map_tf.transform.translation.z = 0.0

        map_tf.transform.rotation.x = 0.0
        map_tf.transform.rotation.y = 0.0
        map_tf.transform.rotation.z = 0.0
        map_tf.transform.rotation.w = 1.0

        self.static_tf_broadcaster.sendTransform(map_tf)

    def update(self):
        """This is the vehicle simulation. It uses the bicycle kinematic model."""
        # get time
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds * 1e-9
        if dt <= 0.0: return
        self.last_time = now

        # set speed
        self.state.velocity = self.commanded_speed

        # update position
        self.state.x += self.state.velocity * math.cos(self.state.yaw) * dt
        self.state.y += self.state.velocity * math.sin(self.state.yaw) * dt

        # update heading
        self.state.yaw += (
            self.state.velocity
            / self.wheelbase
            * math.tan(self.commanded_steering)
            * dt
        )

        # compute odom → base_link
        odom_tf = TransformStamped()

        odom_tf.header.stamp = now.to_msg()
        odom_tf.header.frame_id = "odom"
        odom_tf.child_frame_id = "base_link"

        odom_tf.transform.translation.x = self.state.x
        odom_tf.transform.translation.y = self.state.y
        odom_tf.transform.translation.z = 0.0

        # orientation from yaw
        q = quaternion_from_euler(0.0, 0.0, self.state.yaw)

        odom_tf.transform.rotation.x = q[0]
        odom_tf.transform.rotation.y = q[1]
        odom_tf.transform.rotation.z = q[2]
        odom_tf.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(odom_tf)

        # publish odometry (odom -> base_link)
        odom = Odometry()

        # time stamp
        odom.header.stamp = now.to_msg()

        # frame relationship
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        # position in odom frame
        odom.pose.pose.position.x = self.state.x
        odom.pose.pose.position.y = self.state.y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        # velocity in base_link frame
        odom.twist.twist.linear.x = self.state.velocity
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.linear.z = 0.0
        odom.twist.twist.angular.x = 0.0
        odom.twist.twist.angular.y = 0.0
        odom.twist.twist.angular.z = (
            self.state.velocity / self.wheelbase *
            math.tan(self.commanded_steering)
        )

        # publish
        self.odom_pub.publish(odom)

    def cmd_callback(self, msg):
        """Callback for velocity commands from controller."""

        self.commanded_speed = msg.linear.x
        self.commanded_steering = max(-0.6, min(0.6, msg.angular.z))

        self.get_logger().info(
            f"cmd received: speed={self.commanded_speed:.2f}, "
            f"steering={self.commanded_steering:.2f}, "
            f"raw: linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = VehicleSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
