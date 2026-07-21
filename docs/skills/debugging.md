# Debugging ROS 2 Systems

## Inspect the Graph

Start by verifying that expected nodes and connections exist: `ros2 node list`, `ros2 node info <node>`, `ros2 topic list`, and `rqt_graph`. Use `ros2 doctor --report` to find common environment and middleware problems.

## Inspect Data

Use `ros2 topic echo <topic>` for message fields, `ros2 topic hz <topic>` for rate, and `ros2 topic info -v <topic>` for type and QoS. Validate timestamps, `frame_id`, units, and message freshness before debugging algorithm code.

## Visualize Geometry

Use RViz to inspect `nav_msgs/Path`, odometry, TF axes, and vehicle orientation. `tf2_tools view_frames` exposes TF tree errors. A visual frame or sign error is often easier to find than an algebra error in logs.

## Process Debugging

Increase ROS logger verbosity selectively and keep logs structured. Use GDB for native crashes and a Python debugger for Python nodes. Reduce failures to a recorded input sequence, then add an automated regression test after the cause is fixed.
