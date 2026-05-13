cmake_minimum_required(VERSION 3.4.0)
project(gazebo_grasp_plugin)

find_package(ament_cmake_auto REQUIRED)
find_package(gazebo_dev REQUIRED)
#find_package(gazebo_msgs REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(gazebo_version_helpers REQUIRED)

ament_auto_find_build_dependencies()

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  include
  ${gazebo_version_helpers_INCLUDE_DIRS}
)

# This is used for gazebo message
#add_subdirectory(msgs)

## Declare a cpp library
ament_auto_add_library(gazebo_grasp_fix SHARED
  src/GazeboGraspFix.cpp
  src/GazeboGraspGripper.cpp
)

link_directories(${gazebo_dev_LIBRARY_DIRS})

target_include_directories(gazebo_grasp_fix PUBLIC include)
ament_target_dependencies(gazebo_grasp_fix
  "gazebo_dev"
  "gazebo_ros"
  "gazebo_version_helpers"
)
ament_export_libraries(gazebo_grasp_fix)

## Install
install(TARGETS
  gazebo_grasp_fix
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_package()
