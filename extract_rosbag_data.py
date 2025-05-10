import os
import cv2
import rclpy
import sqlite3
import numpy as np
import rosbag2_py
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

# Define your topics
CAMERA_TOPIC = "/camera/image_raw"
LIDAR_TOPIC = "/scan"

# List of bags and labels
bags = [
    ("low_light", "low_light"),
    ("low_obstacle", "low_obstacle"),
    ("normal", "normal")
]

bridge = CvBridge()

def process_bag(bag_folder, label):
    print(f"Processing {bag_folder}...")

    output_dir = os.path.join("training_data", label)
    os.makedirs(output_dir, exist_ok=True)

    # Connect to SQLite .db3 file
    db_file = os.path.join(bag_folder, "data_0.db3")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get message type for camera and lidar
    msg_types = {
        CAMERA_TOPIC: get_message("sensor_msgs/msg/Image"),
        LIDAR_TOPIC: get_message("sensor_msgs/msg/LaserScan")
    }

    # Create CSV for LIDAR data
    csv_path = os.path.join(output_dir, "lidar_data.csv")
    csv_file = open(csv_path, "w")
    csv_file.write("image_name," + ",".join([f"r{i}" for i in range(360)]) + "\n")

    image_count = 0

    for row in cursor.execute("SELECT topic, data FROM messages ORDER BY timestamp"):
        topic, data = row
        if topic == CAMERA_TOPIC:
            msg = deserialize_message(data, msg_types[CAMERA_TOPIC])
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            image_filename = f"image_{image_count:03d}.png"
            image_path = os.path.join(output_dir, image_filename)
            cv2.imwrite(image_path, cv_image)
        elif topic == LIDAR_TOPIC:
            msg = deserialize_message(data, msg_types[LIDAR_TOPIC])
            if len(msg.ranges) == 0:
                continue
            ranges = np.array(msg.ranges)
            clipped_ranges = np.nan_to_num(ranges, nan=0.0, posinf=0.0, neginf=0.0)
            if image_count > 0:
                csv_file.write(f"image_{image_count-1:03d}.png," + ",".join(map(str, clipped_ranges[:360])) + "\n")
                image_count += 1

    csv_file.close()
    conn.close()
    print(f"Saved {image_count} image + LIDAR pairs in {output_dir}")

def main():
    rclpy.init()
    for bag_folder, label in bags:
        process_bag(bag_folder, label)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
