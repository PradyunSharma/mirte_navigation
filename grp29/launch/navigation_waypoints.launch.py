import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_grp29 = get_package_share_directory('grp29')
    pkg_mirte_navigation = get_package_share_directory('mirte_navigation')

    # Default file paths
    default_map = os.path.join(pkg_grp29, 'maps', 'greenhouse_map.yaml')
    default_waypoints = os.path.join(pkg_grp29, 'config', 'waypoints.yaml')
    default_nav_params = os.path.join(pkg_mirte_navigation, 'params', 'mirte_nav2_params.yaml')

    # Launch arguments (so you can override from command line)
    map_arg = DeclareLaunchArgument('map', default_value=default_map)
    waypoints_arg = DeclareLaunchArgument('waypoints', default_value=default_waypoints)
    params_arg = DeclareLaunchArgument('params_file', default_value=default_nav_params)

    # 1. Laser filter
    laser_filter_node = Node(
        package="laser_filters",
        executable="scan_to_scan_filter_chain",
        parameters=[
            {"use_sim_time": True},
            os.path.join(pkg_grp29, 'laser_config', 'scan_filter.yaml'),
        ],
        remappings=[
            ("scan", "/scan"),
            ("scan_filtered", "/scan_filtered"),
        ],
        output="screen",
    )

    # 2. Map server
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'yaml_filename': LaunchConfiguration('map'),
            'topic_name': 'map',
            'frame_id': 'map',
        }]
    )

    # 3. AMCL for localization
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[LaunchConfiguration('params_file'), {'use_sim_time': True}]
    )

    # 4. Lifecycle manager for map_server + amcl
    lifecycle_manager_localization = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['map_server', 'amcl'],
        }]
    )

    # 5. Nav2 stack
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare("nav2_bringup"), "launch", "navigation_launch.py"
        ])),
        launch_arguments={
            "use_sim_time": "true",
            "params_file": LaunchConfiguration('params_file'),
        }.items()
    )

    # 6. cmd_vel and odom relays
    relay_cmd_vel = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/cmd_vel", "/mirte_base_controller/cmd_vel_unstamped"],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )
    relay_odom = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/mirte_base_controller/odom", "/odom"],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    # 7. base_link → base_footprint
    tf_base_footprint = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "base_footprint"],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    # 8. Waypoint follower script (delayed start so nav2 has time to come up)
    waypoint_follower = TimerAction(
        period=10.0,
        actions=[Node(
            package='grp29',
            executable='waypoint_follower',
            name='waypoint_follower_node',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'waypoints_file': LaunchConfiguration('waypoints'),
            }]
        )]
    )

    # 9. RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", PathJoinSubstitution([
            FindPackageShare("nav2_bringup"), "rviz", "nav2_default_view.rviz"
        ])],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return LaunchDescription([
        map_arg,
        waypoints_arg,
        params_arg,
        laser_filter_node,
        map_server,
        amcl,
        lifecycle_manager_localization,
        navigation_launch,
        relay_cmd_vel,
        relay_odom,
        tf_base_footprint,
        waypoint_follower,
        rviz_node,
    ])