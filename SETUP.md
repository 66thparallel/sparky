# ROS2 Autonomous Vehicle Simulation - Python Dependencies

## Core ROS 2 Python client library
- rclpy

## Message types
- nav_msgs
- geometry_msgs
- ackermann_msgs

## Numerical computing
- numpy
- scipy

## For transforms / kinematics
- transforms3d

## Visualization helpers (optional)
- matplotlib

## Optional: trajectory smoothing / splines
- scikit-learn

## Optional debugging utilities
- tqdm

---

## Setup Instructions

1. Install ROS 2 - Jazzy Jalisco:
   - Follow the official ROS 2 installation guide for your OS.

2. Install ROS 2 message/system dependencies (via apt):
   sudo apt install ros-jazzy-nav-msgs ros-jazzy-geometry-msgs ros-jazzy-ackermann-msgs

3. (Optional) Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install Python dependencies:
   pip install -r requirements.txt

5. Build the ROS 2 workspace:
   colcon build

6. Source the workspace setup script:
   source install/setup.bash

7. Run your ROS 2 nodes as needed.

---

### Notes
- ROS 2 system dependencies (message types) are not installed via pip; use apt as shown above.
- requirements.txt covers only Python dependencies.
- Some dependencies (e.g., rclpy) are installed as part of ROS 2, not via pip.
