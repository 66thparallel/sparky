# Sparky Requirements

## Scope
This document captures the effective requirements for Sparky by combining the stated project intent in the repo documentation with the interfaces and constraints already present in code.

## Product Goal
Build a ROS 2 simulation stack that demonstrates basic autonomous vehicle behavior in 2D:

1. receive or define a route,
2. convert it into a driveable path or trajectory,
3. track that path with a feedback controller,
4. simulate vehicle motion,
5. visualize and evaluate the result.

## Functional Requirements

### Core Motion Stack
- The system must publish a path for the vehicle to follow.
- The system must estimate or publish vehicle state as odometry.
- The controller must consume the desired path and the current vehicle state.
- The controller must output steering and forward-motion commands.
- The simulator must update vehicle pose over time from commanded motion.

### Vehicle Model
- The simulator should support a low-speed kinematic bicycle model.
- The simulator should publish TF for `map`, `odom`, and `base_link`.
- The simulator should publish `nav_msgs/Odometry` for downstream control.

### Planning
- The baseline planner must be able to produce a continuous sequence of waypoints or poses.
- The next planning iteration should support smoother trajectories than a fixed waypoint list.
- The long-term design in the repo notes expects route input plus a planning stage, even though the current implementation uses a parameter-driven waypoint path publisher.

### Control
- The controller should stabilize path tracking using a geometric feedback method.
- The baseline controller may use Pure Pursuit or Stanley control.
- The controller should reduce tracking error while avoiding unstable steering oscillation.

### Visualization and Operator Workflow
- The vehicle description should be available as a URDF asset.
- The system should be launchable in a reproducible way for development.
- RViz visualization is an explicit project goal in the notes and README.

### Logging and Evaluation
- The project notes call for logging and plotting at least:
  - cross-track error,
  - heading error,
  - steering oscillation,
  - control latency,
  - planner loop rate.
- The current implementation publishes controller and planner metrics on dedicated ROS topics and persists them to CSV through `metrics_logger`.
- Performance metrics should be usable for regression tracking and demos.

## Interface Requirements

### Current Topic Contracts
- `/path`: `nav_msgs/Path`
- `/odom`: `nav_msgs/Odometry`
- `/cmd_drive`: `geometry_msgs/Twist`
- `/metrics/controller`: `diagnostic_msgs/DiagnosticArray`
- `/metrics/planner`: `diagnostic_msgs/DiagnosticArray`

### Expected Frame Contracts
- `map`
- `odom`
- `base_link`

## Environment Requirements
- ROS 2 Jazzy Jalisco
- Python 3 with `rclpy`
- ROS message packages including `nav_msgs`, `geometry_msgs`, and related TF packages
- Colcon workspace build support
- A sourced ROS 2 environment before running nodes

The repository also assumes:

- `colcon build` for workspace builds
- `install/setup.bash` sourced before runtime
- local startup via `startup.sh`

## Quality Requirements
- The codebase should stay modular at the package and node level.
- The stack should be understandable as a portfolio-grade demonstration project.
- Package metadata and setup instructions should be complete enough for a new developer to run the workspace.
- Runtime topic names should be internally consistent.

## MVP Acceptance Criteria
The MVP can be considered complete when all of the following are true:

1. the workspace builds cleanly,
2. the path publisher, controller, and simulator run together,
3. the vehicle follows the published path with visibly stable behavior,
4. TF and odometry are valid enough to support visualization,
5. the README and docs explain how to run and evaluate the stack.

## Deferred Requirements
These are documented goals that are not yet fully represented in the current source tree:

1. separate route generation and planning layers,
2. smooth trajectory generation and velocity profiling,
3. richer visualization and launch automation,
4. metrics plotting and packaged analysis outputs,
5. richer route-ingestion and runtime-interface workflows beyond the current parameter-driven MVP.