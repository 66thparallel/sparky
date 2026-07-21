# Control Loops

## Timing

Run each loop at a documented nominal period and compute $dt$ from a monotonic clock. A controller should use the newest valid state, publish one bounded command, and expose missed deadlines or excessive jitter in metrics.

## Sampling Rules

Choose a loop rate much faster than the dynamics being controlled, while respecting CPU and sensor rates. Avoid blocking I/O, unbounded allocation, and expensive planning inside a high-rate callback. Separate lower-rate planning from higher-rate control.

## Limits and Deadbands

- Saturate command magnitude to physical limits.
- Limit command rate to respect actuator dynamics.
- Apply a small deadband only to reject known noise; document it because it creates steady-state error.
- Define a timeout for stale path, odometry, or command data and transition to a safe command.

## Diagnostics

Measure loop period, jitter, state age, command saturation, and tracking error. Deterministic timing and visible failures are more important than a nominally high loop rate.
