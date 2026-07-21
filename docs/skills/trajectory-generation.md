# Trajectory Generation

## From Path to Trajectory

Start with a collision-free geometric path, then produce a time-indexed trajectory that respects velocity, acceleration, steering, and curvature limits. Never ask a controller to follow discontinuous headings or impossible speed changes.

## Waypoints and Splines

Waypoints should be ordered, frame-consistent, and spaced for the expected controller rate. Cubic splines can create smooth position and heading transitions, but check for overshoot near sharp corners or obstacles. Revalidate collision clearance after smoothing.

## Curvature and Speed

For a planar path $y(x)$, curvature is:

$$\kappa = \frac{|y''|}{(1 + y'^2)^{3/2}}$$

Limit speed in turns using lateral acceleration: $v \leq \sqrt{a_{lat,max}/|\kappa|}$. Apply forward and backward passes to also satisfy longitudinal acceleration and braking limits.

## Output Contract

Document frame ID, waypoint spacing, path direction, nominal speed, and whether stops are encoded. If publishing only `nav_msgs/Path`, ensure the controller owns a clear speed policy; otherwise publish a dedicated trajectory message with time and velocity fields.
