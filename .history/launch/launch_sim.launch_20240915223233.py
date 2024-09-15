import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    #Inlcuding robot_state_publisher for our package.
    
    package_name='mobile_bot'

    rsp= IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    #Inlcuding Gazebo launch file from Gazebo_ros package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')])
    )

    #Include the spawner node from the gazebo_ros package
    #This is to spawn robot in Gazebo
    spawn_entity = Node(package='gazebo_ros',executable='spawn_entity.py',
                        arguments=['-topic','robot_description',
                                   '-entity','mobile_bot'],
                        output='screen')
    
    #Launch them all
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])