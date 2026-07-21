# Real-Time Robotics

## Timing Terms

A deadline is the latest acceptable completion time. Jitter is variation in timing around the intended schedule. Deterministic behavior has bounded, predictable timing; a high average rate alone is not real-time behavior.

## Design for Predictability

- Keep control callbacks short and bounded.
- Preallocate or reuse memory in timing-sensitive paths.
- Avoid blocking I/O, unbounded queues, and long lock contention.
- Assign a clear ownership and priority policy to periodic work.
- Measure actual execution time, loop period, state age, and missed deadlines.

## Priority Inversion

Priority inversion occurs when a high-priority task waits for a resource held by a lower-priority task. Reduce shared locks, keep locked regions brief, and use appropriate OS-level synchronization only when needed. ROS 2 executor configuration affects callback scheduling but does not by itself guarantee real-time behavior.

## Sparky Guidance

Treat the simulator and controller loop period as an interface contract. Make timeouts and saturation explicit, log violations, and use simulation metrics to establish a baseline before optimizing runtime behavior.
