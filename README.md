# gazebo_cv

This repos works with ROS2 Humble and Ignition gazebo fortress.

This repository publishes the gazebo camera frame to ROS2 and make is also availble for OpenCV.
Here I have created a simple circle on camera frame.

## How to use

Go to root directory and use colcon to build the repository

```
    colcon build
    source install/setup.bash

    ros2 launch gz_ros_camera world.launch.py

```
The default topic is "camera", which can also be changed from Command line interface.

```
    ros2 launch gz_ros_camera world.launch.py image_topic:=<name of the topic>
```

