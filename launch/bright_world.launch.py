import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Including robot_state_publisher for our package.

    package_name = "mobile_bot"

    # Get the path to the world file
    world_file_path = os.path.join(
        get_package_share_directory(package_name), "worlds", "bright.world"
    )

    # Launch Gazebo directly using gazebo_ros
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
            "world": world_file_path,
            "verbose": "true",
        }.items(),
    )

    # RSP launch
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name), "launch", "rsp.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    # Spawn entity
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "mobile_bot"
        ],
        output="screen",
    )

    # Launch them all
    return LaunchDescription(
        [
            gazebo,
            rsp,
            spawn_entity,
        ]
    )
