# ROS 2 Nodes

## Purpose

A node is a single-purpose ROS 2 process. Keep nodes focused: accept inputs, update local state, and publish outputs. In Sparky, the planner, controller, simulator, and metrics logger are separate Python nodes.

## Create a Python Node

Subclass `rclpy.node.Node`, give it a stable node name, and create interfaces in `__init__`. Use callbacks only to update state or enqueue work; avoid long blocking work in them.

```python
class ExampleNode(Node):
    def __init__(self):
        super().__init__('example_node')
        self.publisher = self.create_publisher(String, '/example', 10)
        self.timer = self.create_timer(0.1, self.publish_status)
```

## Design Rules

- Use descriptive, lowercase names ending in `_node`.
- Validate parameters during startup and fail with an actionable log when invalid.
- Store the latest message from subscriptions; let periodic timers perform predictable control or planning work.
- Use `get_logger()` rather than `print()`.
- Shutdown cleanly with `destroy_node()` and `rclpy.shutdown()`.

## Lifecycle

Use a managed lifecycle node when downstream systems must know whether a component is configured, active, or inactive. For the current MVP, normal nodes are appropriate; add lifecycle management before integrating real hardware or safety-critical startup sequencing.

## Sparky Mapping

`path_planner_node` publishes a route, `controller_node` turns route and odometry into commands, and `vehicle_sim_node` advances simulation state. Preserve that directional data flow when adding nodes.
