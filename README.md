## Sparky - a ROS 2 Real-Time Trajectory Planning and Vehicle Control Stack
Sparky is a modular ROS 2 simulation project for testing basic autonomous vehicle behaviors in a simplified environment.

### Overview

The system simulates a vehicle that:
- Receives a route or waypoint list
- Generates a smooth trajectory
- Tracks the trajectory using a feedback controller
- Visualizes motion in RViz (optional)
- Logs basic performance metrics for analysis

### Architecture
Sparky is split into four core ROS 2 nodes:
- vehicle_sim/ → Simulated vehicle dynamics and state publishing
- path_generator/ → Produces waypoint-based paths
- planner/ → (Optional) higher-level route logic
- controller/ → Pure Pursuit-based path tracking

### Control Approach
The controller uses a Pure Pursuit algorithm for geometric path tracking, converting waypoint lookahead errors into steering commands.

### Data Flow
path_generator → planner → controller → vehicle_sim
                         ↑
                      TF/odom

### Goals
- Four main ROS 2 nodes
- Stable baseline vehicle control
- Easy experimentation with planning and control algorithms
- Can be used for more advanced autonomy features

### Side Story
This project is named after Sparky, Speed Racer's lead mechanic and one of Speed's best friends.