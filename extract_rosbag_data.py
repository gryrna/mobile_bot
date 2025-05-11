import os
import cv2
import rclpy
import sqlite3
import numpy as np

from cv_bridge import CvBridge
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

# Define your topics
CAMERA_TOPIC = "/camera/image_raw"
LIDAR_TOPIC = "/scan"

# Base directory for all bag files and output
base_path = "/home/gryrna/Documents/ros2_ws/src/mobile_bot/ros2_bag_database"

# List of (folder_name, label_name) pairs
bags = [
    ("low_light", "low_light"),
    ("low_obstacle", "low_obstacle"),
    ("normal", "normal")
]

bridge = CvBridge()

def process_bag(bag_folder, label):
    print(f"Processing {bag_folder}...")

    full_bag_path = os.path.join(base_path, bag_folder)
    output_dir = os.path.join(base_path, label)
    os.makedirs(output_dir, exist_ok=True)

    # Connect to SQLite .db3 file inside bag folder
    db_file = os.path.join(full_bag_path, f"{bag_folder}_0.db3")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Dynamically get message types
    msg_types = {
        CAMERA_TOPIC: get_message("sensor_msgs/msg/Image"),
        LIDAR_TOPIC: get_message("sensor_msgs/msg/LaserScan")
    }

    csv_path = os.path.join(output_dir, "lidar_data.csv")
    image_count = 0

    with open(csv_path, "w") as csv_file:
        csv_file.write("image_name," + ",".join([f"r{i}" for i in range(360)]) + "\n")
        
        query = """
                SELECT topics.name, messages.data 
                FROM messages 
                JOIN topics ON messages.topic_id = topics.id 
                ORDER BY messages.timestamp
                """
        for row in cursor.execute(query):
            topic, data = row

            if topic == CAMERA_TOPIC:
                msg = deserialize_message(data, msg_types[CAMERA_TOPIC])
                cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

                image_filename = f"image_{image_count:03d}.png"
                image_path = os.path.join(output_dir, image_filename)
                cv2.imwrite(image_path, cv_image)

                image_count += 1

            elif topic == LIDAR_TOPIC:
                msg = deserialize_message(data, msg_types[LIDAR_TOPIC])
                if len(msg.ranges) == 0:
                    continue

                ranges = np.array(msg.ranges)
                clipped_ranges = np.nan_to_num(ranges, nan=0.0, posinf=0.0, neginf=0.0)

                # Associate this LIDAR data with the previous image
                if image_count > 0:
                    csv_file.write(f"image_{image_count - 1:03d}.png," + ",".join(map(str, clipped_ranges[:360])) + "\n")
                if image_count % 50 == 0:
                    print(f"Saved {image_count} images so far...")


    conn.close()
    print(f"Saved {image_count} image + LIDAR pairs in {output_dir}")

def main():
    rclpy.init()
    for bag_folder, label in bags:
        full_bag_path = os.path.join(base_path, bag_folder)
        db_file = os.path.join(full_bag_path, f"{bag_folder}_0.db3")
        if not os.path.exists(db_file):
            print(f"Database file {db_file} does not exist. Skipping {bag_folder}...")
            continue

        process_bag(bag_folder, label)

    rclpy.shutdown()

if __name__ == "__main__":
    main()
