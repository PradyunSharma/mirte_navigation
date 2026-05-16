# Group 29 - MDP RO47007 - TU Delft 2026
## Digital Twin for Smart Greenhouses

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
ros2 launch mirte_gazebo gazebo_mirte_master_empty.launch.xml world:=~/mdp/src/grp29/sim_world/greenhouse.world
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
ros2 run nav2_map_server map_saver_cli -f explored_map
```
