<<<<<<< README.md
# Group 29 - MDP RO47007 - TU Delft 2026
## Digital Twin for Smart Greenhouses

## Prerequisites
Install all MIRTE Master packages per course instructions before cloning this repo.

## Install & Build
```bash
git clone --recurse-submodules https://gitlab.tudelft.nl/cor/ro47007/2026/group_29.git ~/MDP
cd ~/MDP
sudo apt install ros-humble-laser-filters
rosdep install --from-paths src --ignore-src -r -y
conda deactivate
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run

**Terminal 1:**
```bash
source /opt/ros/humble/setup.bash && source ~/MDP/install/setup.bash
ros2 launch mirte_gazebo gazebo_mirte_master_empty.launch.xml   world:=./src/grp29/sim_world/greenhouse.world
```

**Terminal 2:**
```bash
source /opt/ros/humble/setup.bash && source ~/MDP/install/setup.bash
ros2 launch mirte_navigation explore.launch.py
```

## Save Map
```bash
cd ~/MDP/maps && ros2 run nav2_map_server map_saver_cli -f explored_map
```
