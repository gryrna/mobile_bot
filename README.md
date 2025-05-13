# Mobile Robot Simulation for ROS2 Learning

This repository contains a **mobile robot simulation** designed for understanding the fundamentals of **ROS2** (Robot Operating System 2). The robot features a differential drive system with two powered wheels and a caster wheel for stability, making it perfect for beginners and those looking to learn robot control, sensor integration, and navigation using ROS2.

## Robot Features

The robot is equipped with three essential sensors:

- **LIDAR**: Used for obstacle detection, environment perception, and mapping.
- **Camera**: Provides visual feedback for object detection and recognition.
- **Depth Camera**: Offers depth perception for advanced navigation and obstacle avoidance.

## Project Structure

- **description/**: Contains URDF/XACRO files that define the robot's structure and sensors
  - `robot.urdf.xacro`: Main robot description file
  - `robot_structure.xacro`: Defines the physical structure of the robot
  - `lidar.xacro`, `camera.xacro`, `depth_camera.xacro`: Sensor descriptions
  - `gazebo_control.xacro`: Gazebo control configurations
  - `inertial_macros.xacro`: Inertial property definitions

- **launch/**: Contains launch files for starting the simulation
  - `launch_sim.launch.py`: Main launch file to start Gazebo with the robot
  - `rsp.launch.py`: Robot state publisher configuration

- **worlds/**: Contains Gazebo world definitions
  - `empty.world`: A simple empty world for testing

- **params/**: Contains configuration files for navigation and control

- **test_maps/**: Contains test map files for navigation and localization

## Gazebo Plugins

The simulation leverages several Gazebo plugins to simulate robot functionality:

### 1. Differential Drive Plugin
```xml
<plugin name='diff_drive' filename='libgazebo_ros_diff_drive.so'>
```
- **Purpose**: Controls the robot's movement using a differential drive mechanism
- **Configuration**:
  - Wheel joints: `left_wheel_joint` and `right_wheel_joint`
  - Wheel separation: 0.50 meters
  - Wheel diameter: 0.1 meters
  - Max torque: 200 Nm
  - Max acceleration: 10.0 m/s²
- **Topics**: Publishes odometry data on `/odom` and listens for velocity commands on `/cmd_vel`

### 2. LIDAR Sensor Plugin
```xml
<plugin name="laser_controller" filename="libgazebo_ros_ray_sensor.so">
```
- **Purpose**: Simulates a LIDAR sensor for obstacle detection
- **Configuration**:
  - 180 samples across 90-degree field of view (-45° to +45°)
  - Range: 0.3m to 5m
  - Update rate: 10Hz
  - Visualized in Gazebo for debugging
- **Topics**: Publishes laser scan data on `/scan` in the `lidar_link` frame

### 3. Camera Plugin
```xml
<plugin name="camera_controller" filename="libgazebo_ros_camera.so">
```
- **Purpose**: Simulates a standard RGB camera
- **Configuration**:
  - Resolution: 640×480
  - Field of view: 1.5708 radians (90°)
  - Update rate: 10Hz
- **Topics**: Publishes camera images on `/camera/image_raw` and camera info on `/camera/camera_info`

### 4. Depth Camera Plugin
```xml
<plugin name="depth_camera_controller" filename="libgazebo_ros_camera.so">
```
- **Purpose**: Simulates a depth camera for 3D perception
- **Configuration**:
  - Resolution: 640×480
  - Field of view: 1.5 radians (86°)
  - Update rate: 10Hz
- **Topics**:
  - RGB images: `/depth_camera/image_raw`
  - Camera info: `/depth_camera/camera_info`
  - Depth images: `/depth_camera/depth/image_raw`
  - Depth camera info: `/depth_camera/depth/camera_info`

### 5. System Plugins
The simulation uses these essential Gazebo system plugins:
- `libgazebo_ros_init.so`: Initializes ROS communication in Gazebo
- `libgazebo_ros_factory.so`: Enables spawning of models via ROS services

## Prerequisites

To use this package, you need:

1. ROS2 (Humble or later recommended)
2. Gazebo
3. Required ROS2 packages:
   - gazebo_ros
   - robot_state_publisher
   - xacro

## Building the Package

1. Clone this repository into your ROS2 workspace's `src` directory:
   ```bash
   cd ~/ros2_ws/src
   git clone <repository-url> mobile_bot
   ```

2. Build the package:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select mobile_bot
   ```

3. Source the workspace:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

## Running the Simulation

Launch the robot in Gazebo with:

```bash
ros2 launch mobile_bot launch_sim.launch.py
```

This will start the Gazebo simulator with the robot spawned in an empty world.

## Controlling the Robot

The robot uses a differential drive controller. You can control it using:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.1}}"
```

Or use teleop_twist_keyboard for interactive control:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Sensor Data Visualization

### Visualizing in RViz

To visualize sensor data and robot state in RViz:

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mobile_bot)/share/mobile_bot/rviz_mobile_bot.rviz
```

Or load the provided configuration file manually.

### Viewing Camera Images

```bash
ros2 run rqt_image_view rqt_image_view
```

### Viewing LIDAR Data

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix mobile_bot)/share/mobile_bot/rviz_mobile_bot.rviz
```

![mobile_bot](rviz_screenshot_2024_09_17-10_16_23.png)

## Data Logging

The robot simulation can be used with the `data_logger` package to record sensor data. See the [data_logger](../data_logger/README.md) package for more information.

## Future Development

- Adding navigation stack configuration
- Implementing SLAM capabilities
- Creating more complex world environments
- Adding sensor processing algorithms
- Integration with machine learning frameworks

## Troubleshooting

If you encounter any issues with the simulation:

1. Ensure all dependencies are installed
2. Check that your ROS2 environment is properly sourced
3. Verify that the Gazebo plugins are correctly installed
4. Check ROS topic availability with `ros2 topic list`
