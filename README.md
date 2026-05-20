# Group 29 - MDP RO47007 - TU Delft 2026
## Digital Twin for Smart Greenhouses

## Introduction to the repository
This repository contains our developed ROS2 packages (for example `grp29`) and ROS2 packages as submodules (including `clearpath_mecanum_drive_controller`,  `gazebo_grasp_fix`, `mirte-gazebo`, `mirte-ros-packages`, `mirte_navigation`, `ros2_astra_camera` and `rplidar_ros`). Out of all the sub modules, `mirte-gazebo`, `mirte_navigation` and `mirte-ros-packages` are forked thus their code can be modified. For rest of the modules, the code cannot be modifies as the are purely submodules. If you do modify their code, it would only be on your local system. In case it is required to modify their code, those submodules need to be forked and gid needs to point to the forked repositories.

## Prerequisites
Have ROS2 and Gazebo installed as per course instructions.

## Generate ROS2 workspace
```bash
mkdir -p mdp
cd mdp
```

## Clone this repository
While inside `mdp` directory do:
```bash
# By SSH
git clone git@gitlab.tudelft.nl:cor/ro47007/2026/group_29/mdp.git
# By URL
git clone https://gitlab.tudelft.nl/cor/ro47007/2026/group_29/mdp.git
```
Now clone the submodules by:
```bash
git submodule update --init --recursive
```

## Rename
As the repo is called `mdp`, the cloned folder is also called `mdp`, this needs to be renamed as `src`.
```bash
mv mdp src
```

## Build and source
Build from root of the ros2 workspace, that is `mdp`. Do not forget to **source ROS2** first `source /opt/ros/humble/setup.bash`.

```bash
colcon build --symlink-install
source install/setup.bash
```

## Run the simulation
While inside `mdp`:
```bash
ros2 launch mirte_gazebo gazebo_mirte_master_empty.launch.xml world:=/home/"your_pc_name"/mdp/src/grp29/sim_world/greenhouse.world

```
Note: You pass the location of `greenhouse.world` file as parameter.
This will launch the gazebo simulation.

Now open a new terminal and `cd` to `mdp` directory.
```bash
source install/setup.bash
ros2 launch mirte_navigation explore.launch.py
```
This will run the SLAM and map can be visualized in the Rviz.

To save map:
```bash
cd src/grp29/maps
ros2 run nav2_map_server map_saver_cli -f ~/mdp/src/grp29/maps/greenhouse_map
```
## Run waypoint follower
These instructions allow the robot to follow waypoint in a saved map via nav2. \
In first terminal
```bash
cd ~/mdp
source install/setup.bash
ros2 launch mirte_gazebo gazebo_mirte_master_empty.launch.xml world:=/home/"your_pc_name"/mdp/src/grp29/sim_world/greenhouse.world # Run the gazebo simulation first
``` 
Open a new terminal
```bash
cd ~/mdp
source install/setup.bash
ros2 launch grp29 navigation_waypoints.launch.py # Run the waypoint navigation launch file
# Optionally you can also pass the custom files (map and waypoint list) at launch time
ros2 launch grp29 navigation_waypoints.launch.py waypoints:=/path/to/my_waypoints.yaml map:=/path/to/my_map.yaml
```
`navigation_waypoints.launch.py` picks uo the saved map `mdp/src/grp29/sim_world/greenhouse.world` and the waypoints listed in `waypoints.yaml` file. Curretly, the waypoints are randomly places in the map, later these poins will be generated around the plant pots by a script. 

