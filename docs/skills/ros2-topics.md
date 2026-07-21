# ROS 2 Topics

## Topic Design

Topics carry continuous, asynchronous streams. Use one topic for one clearly defined data product and use standard message types where possible. Sparky uses `/path` (`nav_msgs/Path`), `/odom` (`nav_msgs/Odometry`), and `/cmd_drive` (`geometry_msgs/Twist`).

## Naming

- Prefer lowercase `snake_case` names.
- Use a leading `/` only for globally scoped, system-level topics.
- Use relative names inside reusable nodes so a launch file can namespace them.
- Make units clear through the message definition or documentation; ROS SI units are expected.

## QoS Selection

| Data | Recommended starting QoS |
| --- | --- |
| Command and sensor streams | `reliable`, `keep_last` with a small depth |
| High-rate lossy sensors | `best_effort` when freshness is more important than delivery |
| Static configuration or map | `transient_local` so late joiners receive the last value |

Publisher and subscriber QoS settings must be compatible. Match QoS deliberately rather than relying on defaults.

## Rates and Debugging

Publish at a rate appropriate to the consumer. A controller should run at a stable, documented rate; a path can publish less often but must be available before tracking starts. Inspect traffic with `ros2 topic list`, `ros2 topic info -v`, `ros2 topic echo`, and `ros2 topic hz`.

Avoid logging every message at high rates. Log transitions, invalid inputs, or rate-limited diagnostics instead.
