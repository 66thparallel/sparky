# Path Following

## Controller Selection

| Method | Strength | Main limitation |
| --- | --- | --- |
| Pure Pursuit | Simple, stable, geometric | Requires lookahead tuning |
| Stanley | Strong heading and cross-track correction | Sensitive to low speed and tuning |
| MPC | Handles constraints and prediction | Higher model and compute cost |
| PID steering | Simple actuator correction | Does not understand path geometry alone |

## Pure Pursuit

Pure Pursuit selects a target point ahead of the vehicle. For wheelbase $L$, lookahead distance $L_d$, and target angle $\alpha$, a common steering command is:

$$\delta = \arctan\left(\frac{2L\sin\alpha}{L_d}\right)$$

Use a speed-dependent, bounded lookahead. Too short causes oscillation; too long cuts corners and responds slowly.

## Implementation Checks

- Transform the target point into `base_link` before calculating steering.
- Find the closest valid forward path point and handle end-of-path stopping explicitly.
- Saturate steering, speed, and steering rate according to the vehicle model.
- Publish safe commands if path or odometry becomes stale.

Sparky currently uses pure pursuit. Record cross-track error, heading error, lookahead, and command saturation in metrics before replacing it with a more complex controller.
