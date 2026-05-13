import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_mirte_navigation = get_package_share_directory('mirte_navigation')

    params_file = os.path.join(
        pkg_mirte_navigation, 'params', 'mirte_nav2_params.yaml'
    )

    # 1. Laser filter
    laser_filter_node = Node(
        package="laser_filters",
        executable="scan_to_scan_filter_chain",
        parameters=[
            {"use_sim_time": True},
            "/home/fn8211/MDP/laser_config/scan_filter.yaml",
        ],
        remappings=[
            ("scan", "/scan"),
            ("scan_filtered", "/scan_filtered"),
        ],
        output="screen",
    )

    # 2. SLAM
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare("slam_toolbox"), "launch", "online_async_launch.py"
        ])),
        launch_arguments={
            "use_sim_time": "true",
            "slam_params_file": "/home/fn8211/MDP/slam_config/mirte_slam.yaml",
        }.items()
    )

    # 3. Nav2
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare("nav2_bringup"), "launch", "navigation_launch.py"
        ])),
        launch_arguments={
            "use_sim_time": "true",
            "params_file": params_file,
        }.items()
    )

    # 4. cmd_vel relay
    relay_cmd_vel = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/cmd_vel", "/mirte_base_controller/cmd_vel_unstamped"],
        output="screen",
    )

    # 5. odom relay
    relay_odom = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/mirte_base_controller/odom", "/odom"],
        output="screen",
    )

    # 6. base_link → base_footprint
    tf_base_footprint = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "base_footprint"],
        output="screen",
    )

    # 7. explore
    explore_node = TimerAction(
        period=8.0,
        actions=[Node(
            package="explore_lite",
            executable="explore",
            name="explore_node",
            output="screen",
            parameters=[{
                "use_sim_time": True,
                "robot_base_frame": "base_link",
                "costmap_topic": "/global_costmap/costmap",
                "costmap_updates_topic": "/global_costmap/costmap_updates",
                "visualize": True,
                "planner_frequency": 0.1,
                "progress_timeout": 20.0,
                "potential_scale": 3.0,
                "orientation_scale": 0.0,
                "gain_scale": 1.0,
                "transform_tolerance": 0.3,
                "min_frontier_size": 0.3,
            }]
        )]
    )

    # 8. RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", PathJoinSubstitution([
            FindPackageShare("nav2_bringup"), "rviz", "nav2_default_view.rviz"
        ])],
        output="screen",
    )

    return LaunchDescription([
        laser_filter_node,
        slam_launch,
        navigation_launch,
        relay_cmd_vel,
        relay_odom,
        tf_base_footprint,
        explore_node,
        rviz_node,
    ])
