cmake_minimum_required(VERSION 3.8)
project(gz_ros_camera)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(OpenCV REQUIRED)


#install 
install(DIRECTORY launch rviz models worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
