import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = "mobile_bot"

    # Get the path to the world file
    world_file_path = os.path.join(
        get_package_share_directory(package_name), "worlds", "fog.world"
    )

    # Start gzserver with SystemPlugins
    gzserver = ExecuteProcess(
        cmd=[
            "gzserver",
            world_file_path,
            "-s", "libgazebo_ros_init.so",
            "-s", "libgazebo_ros_factory.so",
            "--verbose"
        ],
        output="screen"
    )

    # Optional: Start gzclient (UI)
    gzclient = ExecuteProcess(
        cmd=["gzclient"],
        output="screen"
    )

    # Robot State Publisher launch
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name), "launch", "rsp.launch.py"
            )
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    # Spawn the robot in Gazebo
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "mobile_bot"
        ],
        output="screen",
    )

    return LaunchDescription([
        gzserver,
        gzclient,
        rsp,
        spawn_entity
    ])
