import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatusArray, GoalStatus
import subprocess
import os

class ExploreWatchdog(Node):
    def __init__(self):
        super().__init__('explore_watchdog')
        self.triggered = False

        self.sub = self.create_subscription(
            GoalStatusArray,
            '/navigate_to_pose/_action/status',
            self.cb,
            10,
        )
        self.get_logger().info(
            "Watching /navigate_to_pose/_action/status for CANCELED..."
        )

    def cb(self, msg):
        if self.triggered:
            return
            
        if not msg.status_list:
            return
        latest = msg.status_list[-1]
        if latest.status == GoalStatus.STATUS_CANCELED:
            self.triggered = True
            self.get_logger().info("Goal CANCELED detected. Saving map...")
            self.run_pipeline()

    def run_pipeline(self):
        here = os.path.dirname(os.path.abspath(__file__))
        map_prefix = os.path.join(here, "my_map")
        script = os.path.join(here, "obstacle_size.py")

        subprocess.run(
            ["ros2", "run", "nav2_map_server", "map_saver_cli",
             "-f", map_prefix],
            check=False,
        )
        subprocess.run(["python3", script], check=False)
        self.get_logger().info("Done.")
        rclpy.shutdown()


def main():
    rclpy.init()
    rclpy.spin(ExploreWatchdog())


if __name__ == "__main__":
    main()
