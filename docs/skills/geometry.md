# Robotics Geometry

## Vectors

For vectors $a$ and $b$, the dot product $a\cdot b$ measures alignment and the 2D scalar cross product $a_xb_y-a_yb_x$ gives signed turning direction. Normalize only nonzero vectors and preserve units throughout calculations.

## Angles

Normalize heading differences to $[-\pi, \pi)$ to prevent discontinuities at the wrap boundary:

$$\operatorname{wrap}(\theta)=((\theta+\pi) \bmod 2\pi)-\pi$$

Use `atan2(y, x)` for quadrant-safe angles. Keep internal angles in radians and convert only at user-facing boundaries.

## Coordinate Transforms

A 2D pose transform combines rotation and translation. To express point $p$ in frame $A$ from frame $B$:

$$p_A = R_{AB}p_B+t_{AB}$$

State source and destination frames explicitly. In ROS, prefer TF2 for runtime frame conversion rather than duplicating transform math in unrelated nodes.
