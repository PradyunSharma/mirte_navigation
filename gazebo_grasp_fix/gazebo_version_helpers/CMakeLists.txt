cmake_minimum_required(VERSION 3.4.0)
project(gazebo_version_helpers)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

find_package(gazebo_dev REQUIRED)
find_package(gazebo_ros REQUIRED)

###########
## Build ##
###########

ament_auto_add_library(${PROJECT_NAME} SHARED
  src/GazeboVersionHelpers.cpp
)

link_directories(${gazebo_dev_LIBRARY_DIRS})

target_include_directories(${PROJECT_NAME} PUBLIC include)
ament_target_dependencies(${PROJECT_NAME}
  "gazebo_dev"
  "gazebo_ros"
)
ament_export_libraries(${PROJECT_NAME})

## Install
install(TARGETS
  ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_export_include_directories(
  include
)

#############
## Install ##
#############

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
)

ament_package()
