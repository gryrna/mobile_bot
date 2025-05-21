# 🔧 ROS 2 + Gazebo Sensor Fusion Dataset Automation (GPT-4o)

## 🧠 CONTEXT

We're building a dataset for a **neural network-based sensor fusion project** in **ROS 2 with Gazebo Classic**, using a **two-wheeled differential-drive robot** equipped with **LIDAR and camera**. The robot is placed in simulation environments with various **obstacles** and **scene conditions**, and the system automatically collects synchronized sensor data and ground truth distances.

The final goal is to generate **2,875 labeled samples** across 5 environments and 23 object types.

---

## ✅ CURRENT SETUP

**Robot & Simulation:**

- ROS 2 workspace: `/home/gryrna/Documents/ros2_ws/`
- Robot package: `mobile_bot`
  - Contains launch files (`launch/`), robot URDF(`description/`), and `rsp.launch.py`
  - Simulation starts in an **empty world**, robot spawns at `(0, 0, 0)`
- Environment files (`*.world`) exist for: `bright`, `dark`, `foggy`, `low_light`, `dusty`

**Obstacle Models:**

- 23 total SDF models categorized as:
  - **Normal**: Cabinet , Car wheel , Cardboard Box , Cinder block new , Construction Barrel , Construction Cone
  - **Thin objects**:Fire Hydrant , Jersey barrier , Mailbox ,Standing Person
  - **Large**: Hatchback, Dumpster
  - **Small**: Beer ,Black_ball ,Black_ball_transparent ,Cinder block wide ,Coke Can ,Green ball ,Red Ball
  - **Transparent**: Transparent_Cone ,Transparent_sheet ,Mesh ,Mesh round
- Stored in: `~/.gazebo/models/{model_name}/model.sdf`

**Data Logger System:**

- Package: `data_logger`
  - Nodes: `data_logger_node`, `ground_truth_listener`, `scene_spawner`
  - Folder: `/home/gryrna/Documents/ros2_ws/src/data_logger`
- Logging topics:
  - `/camera/image_raw`
  - `/scan`
- Ground truth extracted via `/ground_truth/distance` and `/ground_truth/angle`

**Synchronization Mechanism:**

- Nodes communicate using:
  - `/obstacle_ready` (from spawner → ground truth logger)
  - `/trigger_sample` (from controller → logger)

**Config file:**
- YAML file listing `obstacle` and `scene_condition` pairs
- Used to drive sample generation

---

## 🔄 OBJECTIVE

We want to **automate** the data collection pipeline using a YAML configuration and collect a total of 2,875 high-quality data samples. Each sample should log:
- Camera frame
- LIDAR scan
- Ground truth distance to obstacle
- Timestamp
- Metadata (obstacle type, size, environment, etc.)

---

## 🛠️ REQUIRED TASKS

### 1. ✅ Review & Improve Existing ROS 2 Files

**Review the following files:**

- `mobile_bot/launch/*.py`
  - Launches Gazebo with selected world
  - Spawns robot using `spawn_entity.py`
  - Starts robot_state_publisher
- `data_logger/launch/data_collection.launch.py`
  - Launches `scene_spawner`, `data_logger`, and `ground_truth_listener`
- `data_logger/config/config.yaml`
- `data_logger/data_logger/*.py`
  - `scene_spawner`: spawns selected model
  - `data_logger`: logs camera + LIDAR + scene
  - `ground_truth_listener`: listens to /model_states and publishes ground truth

---

### 2. ✅ Finalize YAML Structure

**Redesign `config.yaml` as:**

```yaml
samples:
  - obstacle: transparent_cone
    environment: foggy
    pose:
      x: 3.0
      y: 0.0
      z: 0.0
    count: 5
  - obstacle: hatchback
    environment: dusty
    pose:
      x: 4.5
      y: 1.0
      z: 0.0
    count: 5
  # ...repeat for all 2,875 samples
````

Use this to drive automated launch + logging.

---

### 3. ✅ Build Master Control Script (Python or Bash)

Create a script `run_batch_collection.py` that will:

* Loop over each config entry
* Launch Gazebo with correct world file (e.g., `dusty.world`)
* Launch ROS 2 nodes via `data_collection.launch.py`
* Send `/trigger_sample` once `/obstacle_ready` is received
* Wait until logging is done (or timeout)
* Save data to `/data_samples/{sample_id}/`
* Record metadata file in each folder

---

### 4. ✅ Ensure Each Sample Logs:

Inside each sample folder:

```
scene_00042/
  image.png
  scan.csv
  ground_truth.json
  metadata.yaml
```

* **image.png** from `/camera/image_raw`
* **scan.csv** from `/scan`
* **ground_truth.json** = obstacle name, exact position, estimated distance, estimated angle
* **metadata.yaml** = timestamp, obstacle, environment, category, etc.

---

### 5. ✅ Environment Switching Logic

Allow world file/environment to be swapped dynamically from launch script:

```bash
ros2 launch mobile_bot main_launch.py world:=dusty.world
```

or equivalent.

If not supported, refactor `main_launch.py` to accept `world` as launch argument.

---

### 6. ✅ Refactor `scene_spawner`

* Accept parameters: model name, pose
* Load model from `~/.gazebo/models/{name}/model.sdf`
* Publish `/obstacle_ready` after spawn

---

### 7. ✅ Add Fail-Safe Logic

* Timeout if `/obstacle_ready` not received in X seconds
* Skip sample if logging nodes crash
* Optionally allow resume from last successful sample

---

## 🔁 WHAT TO DO NOW

1. ✅ Review all existing code in `mobile_bot` and `data_logger` package
2. ✅ Validate and improve:

   * Launch files
   * Nodes
   * YAML schema
3. ✅ Write the `run_batch_collection.py` script
4. ✅ Add CLI usage or log summary if helpful
5. ✅ Ensure it's modular, failsafe, and reusable

---

## 📁 OUTPUT FOLDERS

Store output in:

```
ros2_ws/
└── data_samples/
    ├── scene_00001/
    ├── scene_00002/
    └── ...
```

---

## 🧾 SAMPLE METADATA STRUCTURE (metadata.yaml)

```yaml
scene_id: 42
timestamp: 2025-05-19T14:32:11Z
obstacle: transparent_cone
environment: foggy
pose:
  x: 3.0
  y: 0.0
  z: 0.0
ground_truth_distance: 2.37
notes: "Edge case: transparent + fog"
```

---

## ✅ ASSUME

* ROS 2 Humble
* Gazebo Classic (Gazebo-11)
* `rclpy`, `gazebo_ros`, and `gazebo_msgs` available
* `ros2 launch` and topic introspection (`rqt`, `ros2 topic echo`) work as expected

---

> Now, review the project and begin implementing all required files, scripts, and improvements.

```