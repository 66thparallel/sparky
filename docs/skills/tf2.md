# TF2 Coordinate Transforms

## Frame Conventions

TF describes the geometric relationship between coordinate frames over time. Use right-handed frames and ROS conventions: $x$ forward, $y$ left, and $z$ up for `base_link`. Use meaningful, stable names such as `map`, `odom`, and `base_link`.

Sparky's expected chain is:

```text
map → odom → base_link
```

`map` is globally consistent, `odom` is locally smooth but may drift, and `base_link` is attached to the vehicle.

## Static and Dynamic Transforms

Publish fixed geometry, such as sensor mounting offsets, once with `StaticTransformBroadcaster`. Publish moving relationships, such as `odom` to `base_link`, repeatedly with a timestamp matching the state estimate. A transform tree must have one parent per child and no cycles.

## Common Mistakes

- Reversing parent and child frame IDs.
- Publishing a pose in one frame while labeling it as another.
- Mixing degrees with radians or milliseconds with seconds.
- Looking up a transform at a timestamp for which no data exists.
- Having multiple nodes publish the same transform edge.

## Debugging

Run `ros2 run tf2_tools view_frames` to inspect the tree, `ros2 run tf2_ros tf2_echo <target> <source>` to inspect a transform, and RViz to validate axes visually. Check `header.frame_id`, `child_frame_id`, timestamps, and transform direction before changing controller math.
