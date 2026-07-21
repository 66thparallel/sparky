# ROS 2 Launch Files

## Purpose

Launch files compose nodes into a reproducible system. A single launch description should start Sparky's planner, controller, simulator, and metrics logger with consistent parameters and remappings.

## Core Patterns

- Use Python launch files for conditional logic, substitutions, and reusable groups.
- Declare launch arguments for settings a user may vary, such as a route file, simulator rate, or namespace.
- Load parameters from YAML files rather than embedding many values in the launch file.
- Pass `output='screen'` during development so node logs are visible.

## Namespaces and Remapping

Namespace a complete vehicle instance with `PushRosNamespace`, then use relative topic names within components. Remap only at integration boundaries; do not bake deployment-specific topic names into node code.

```python
Node(
    package='controller', executable='controller_node',
    name='controller_node', namespace=LaunchConfiguration('vehicle_ns'),
    parameters=[LaunchConfiguration('params_file')],
    remappings=[('/path', 'path')],  # resolve global topic into the node's namespace
)
```

## Parameter Files

Keep YAML organized by node name, include units in comments or parameter descriptions, and make defaults safe. Validate required values in node startup because a parameter file can be malformed or overridden.
