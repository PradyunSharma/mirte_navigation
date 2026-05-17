#!/usr/bin/env python3
import rclpy
import yaml
import math
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener


def yaw_to_quaternion(yaw):
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


class WaypointFollower(Node):
    def __init__(self):
        super().__init__('waypoint_follower_node')

        self.declare_parameter('waypoints_file', '')
        waypoints_file = self.get_parameter('waypoints_file').value

        if not waypoints_file:
            self.get_logger().error("No waypoints_file parameter provided!")
            return

        self.waypoints = self.load_waypoints(waypoints_file)
        self.get_logger().info(f"Loaded {len(self.waypoints)} waypoints from {waypoints_file}")

        # TF buffer to check for map -> odom transform
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.current_idx = 0
        self.wait_for_localization_and_start()

    def load_waypoints(self, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('waypoints', [])

    def wait_for_localization_and_start(self):
        self.get_logger().info("Waiting for navigate_to_pose action server...")
        self.action_client.wait_for_server()

        self.get_logger().info("Waiting for map -> odom transform (AMCL localization)...")
        # Use a timer to check repeatedly
        self.localization_timer = self.create_timer(1.0, self.check_localization)

    def check_localization(self):
        try:
            self.tf_buffer.lookup_transform('map', 'odom', rclpy.time.Time())
            self.get_logger().info("Localization ready! Sending first waypoint.")
            self.localization_timer.cancel()
            self.send_next_waypoint()
        except Exception:
            self.get_logger().info("Still waiting for map -> odom transform...")

    def send_next_waypoint(self):
        if self.current_idx >= len(self.waypoints):
            self.get_logger().info("All waypoints completed!")
            return

        wp = self.waypoints[self.current_idx]
        self.get_logger().info(
            f"Sending waypoint {self.current_idx + 1}/{len(self.waypoints)}: "
            f"({wp['x']}, {wp['y']}, yaw={wp.get('yaw', 0.0)})"
        )

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = float(wp['x'])
        goal_msg.pose.pose.position.y = float(wp['y'])
        goal_msg.pose.pose.position.z = 0.0

        qx, qy, qz, qw = yaw_to_quaternion(float(wp.get('yaw', 0.0)))
        goal_msg.pose.pose.orientation.x = qx
        goal_msg.pose.pose.orientation.y = qy
        goal_msg.pose.pose.orientation.z = qz
        goal_msg.pose.pose.orientation.w = qw

        send_goal_future = self.action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn(f"Waypoint {self.current_idx + 1} rejected, skipping")
            self.current_idx += 1
            self.send_next_waypoint()
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result()
        if result.status == 4:
            self.get_logger().info(f"Waypoint {self.current_idx + 1} reached!")
        else:
            self.get_logger().warn(f"Waypoint {self.current_idx + 1} failed with status {result.status}")

        self.current_idx += 1
        self.send_next_waypoint()


def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()