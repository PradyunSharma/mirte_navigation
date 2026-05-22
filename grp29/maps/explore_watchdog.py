import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatusArray, GoalStatus
from std_msgs.msg import String
import subprocess
import os
import time

class ExploreWatchdog(Node):
    def __init__(self):
        super().__init__('explore_watchdog')
        self.triggered = False
        self.last_goal_time = None
        self.sub = self.create_subscription(
            GoalStatusArray,
            '/navigate_to_pose/_action/status',
            self.cb,
            10,
        )
        # if no new goal in 15s, then exit
        self.timer = self.create_timer(5.0, self.check_idle)
        self.get_logger().info("Watchdog started...")

    def cb(self, msg):
        if self.triggered:
            return
        if msg.status_list:
            self.last_goal_time = time.time()

    def check_idle(self):
        if self.triggered:
            return
        if self.last_goal_time is None:
            return
        # if no new goal in 15s, then exit
        if time.time() - self.last_goal_time > 15.0:
            self.triggered = True
            self.get_logger().info("No new goals for 15s. Saving map...")
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
