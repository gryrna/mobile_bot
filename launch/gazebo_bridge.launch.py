#ROS2 Gazebo Bridge to communicate with ROS2 from Gazebo

import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    package_name = "mobile_bot"

    # Launch Gazebo with ROS bridge support
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py",
                )
            ]
        ),
        launch_arguments={
            "world": os.path.join(
                get_package_share_directory(package_name), "worlds", "my_world.world"
            ),
            "verbose": "true",
            "extra_gazebo_args": "--ros-args --params-file "
            + os.path.join(
                get_package_share_directory("gazebo_ros"),
                "config",
                "gazebo_params.yaml",
            ),
        }.items(),
    )

    # Add the ROS-Gazebo bridge
    gazebo_ros_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        arguments=[
            "/model/info@gz.msgs.Model@ros_gz_interfaces.msg.Model",
            "/world/default/model/info@gz.msgs.Model@ros_gz_interfaces.msg.Model",
        ],
        output="screen",
    )

    return LaunchDescription([gazebo, gazebo_ros_bridge])
