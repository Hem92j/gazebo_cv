import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_gz_ros_camera = get_package_share_directory('gz_ros_camera')

    image_topic_value = LaunchConfiguration("image_topic")

    image_topic_arg = DeclareLaunchArgument("image_topic",
                                            default_value="camera")

    sdf_file = os.path.join(pkg_gz_ros_camera, 'worlds', 'demo_world.sdf')

    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()

    # robot state pubisher(not in the use )
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    # run ignition gazebo
    ign = ExecuteProcess(
        cmd=[
            'ign', 'gazebo', '-r',
            os.path.join(
                pkg_gz_ros_camera,
                'worlds',
                'actor_world.sdf'
            )
        ]
    )

    # initialize bridge between ignition gazebo and ros2
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/camera@sensor_msgs/msg/Image@ignition.msgs.Image",
            "/lidar@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan",
            "/lidar/points@sensor_msgs/msg/PointCloud2@ignition.msgs.PointCloudPacked"
        ],
        output="screen"
    )

    # start rviz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d', os.path.join(pkg_gz_ros_camera, 'rviz', 'gz_ros_test.rviz')]
    )

    # gazebo to opencv bridge via ros2
    # change the image_topic value as required
    gz_cv_faster = Node(
        package="ros_cv_camera",
        executable="human_faster",
    )

    gz_cv = Node(
        package="ros_cv_camera",
        executable="img_sub",
        parameters=[
            {"image_topic": image_topic_value}
        ],

    )

    return LaunchDescription([
        ign,
        bridge,
        rviz,
        image_topic_arg,
        # gz_cv,
        gz_cv_faster
    ])
