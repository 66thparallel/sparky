# Sparky Setup

## Setup Instructions

1. Install ROS 2 Jazzy Desktop and the runtime tools Sparky uses.

   ```sh
   sudo apt update
   sudo apt install -y \
     ros-jazzy-desktop \
     python3-colcon-common-extensions \
     ros-jazzy-robot-state-publisher \
     ros-jazzy-tf-transformations \
     ros-jazzy-tf2-tools
   ```

2. From the Sparky workspace root, source ROS 2 and build the workspace.

   ```sh
   cd ~/projects/sparky
   source /opt/ros/jazzy/setup.bash
   colcon build --symlink-install
   ```

3. In the same terminal, source the built workspace and launch the full stack with the default route.

   ```sh
   source install/setup.bash
   ros2 launch path_planner sparky.launch.py
   ```

4. In a second terminal, source ROS 2 and the workspace again, then open RViz with the checked-in config.

   ```sh
   cd ~/projects/sparky
   source /opt/ros/jazzy/setup.bash
   source install/setup.bash
   rviz2 -d $(ros2 pkg prefix path_planner)/share/path_planner/rviz/sparky.rviz
   ```

5. If you want to test a different route, keep the same launch file and point it at another YAML route config.

   ```sh
   ros2 launch path_planner sparky.launch.py \
     route_config:=/absolute/path/to/your_route.yaml
   ```
