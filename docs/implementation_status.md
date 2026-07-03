# Sparky Implementation Status

## Summary
Sparky is currently in MVP-in-progress state. The core closed loop, launch wiring, and CSV-backed metrics pipeline exist in code, but the implementation is still narrower than the documented target architecture and several production-readiness items are still missing.

## Status by Area

| Area | Status | Notes |
| --- | --- | --- |
| Workspace structure | Implemented | `src/` contains `path_planner`, `controller`, `vehicle_sim`, `vehicle_description`, and `metrics_logger` as the active package set for the current stack. |
| Path publication | Implemented | `path_planner_node` publishes a `nav_msgs/Path` in the `map` frame from configurable waypoint parameters. |
| Tracking controller | Implemented | `controller_node` subscribes to `/path` and `/odom` and publishes `/cmd_drive` using a pure-pursuit-style loop. |
| Vehicle simulation | Implemented | `vehicle_sim_node` integrates a kinematic bicycle model and publishes odometry plus TF. |
| RViz visualization | Implemented | RViz can display the moving vehicle when the runtime nodes, `robot_state_publisher`, and RViz are started manually or via the checked-in config. |
| Vehicle description | Partial | URDF exists, but it is currently a minimal box model only. |
| Route ingestion | Partial | `path_planner_node` accepts waypoint input through ROS parameters or a launch-selected YAML file at startup, but there is no richer external route ingestion pipeline yet. |
| Trajectory generation | Missing | No smoothing, time parameterization, or velocity profile generation is implemented. |
| Launch orchestration | Partial | `path_planner/launch/sparky.launch.py` starts `vehicle_sim_node`, `controller_node`, `path_planner_node`, `robot_state_publisher`, and `metrics_logger`, but RViz is still started separately. |
| RViz configuration asset | Implemented | `path_planner/rviz/sparky.rviz` provides a reusable workspace config for the current stack. |
| Metrics and logging | Partial | Controller and planner metrics topics are published, `metrics_logger` writes CSV files plus periodic summaries, and the launch path starts the logger by default; plots and deeper analysis outputs are still missing. |
| Package metadata | Implemented | Package descriptions, runtime dependencies, and MIT license fields are declared across the active packages. |

## Implemented Today

### `path_planner`
- Publishes `/path` once per second.
- Accepts configurable waypoint input through the `waypoints` parameter or a launch-selected YAML file.
- Gives the rest of the stack a deterministic path source for testing.

### `controller`
- Waits for both odometry and a path before commanding motion.
- Selects the first waypoint at or beyond the configured lookahead distance.
- Computes curvature from heading error and converts it into `Twist` commands.

### `vehicle_sim`
- Maintains internal vehicle state: `x`, `y`, `yaw`, and velocity.
- Applies a bicycle-model update each timer tick.
- Uses `/cmd_drive` as its single command input.
- Publishes `Odometry` and TF for downstream consumers and visualization.

### `vehicle_description`
- Installs `urdf/vehicle.urdf` with a single `base_link` visual.
- Provides a placeholder visual model rather than a detailed robot description.
- Supports manual RViz visualization when paired with `robot_state_publisher`.
- Can be viewed with the checked-in `sparky.rviz` config.

### `metrics_logger`
- Subscribes to `/metrics/controller` and `/metrics/planner`.
- Writes controller and planner CSV files to a configurable log directory.
- Emits low-rate human-readable summaries for demos and regressions.

## Notable Gaps and Risks

### Historical planning notes differ from the current runtime
- Earlier project notes describe a `path_generator` plus `planner` split. The current implemented runtime uses a single `path_planner` package backed by configurable waypoint input.
- That is a design-history difference.

## Recommended Next Steps

1. Add plotting or packaged analysis outputs on top of the current CSV metrics pipeline.
2. Extend configurable waypoint input into richer route ingestion or planning if the project grows beyond the current parameter-driven route source.
3. Continue aligning any remaining historical notes with the current `path_planner`-based runtime.