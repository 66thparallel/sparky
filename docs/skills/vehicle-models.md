# Vehicle Models

## Match the Model to the Vehicle

Kinematic models describe geometry and are suitable at low speed where tire slip is negligible. Dynamic models include forces, inertia, and tire behavior and are needed when acceleration, slip, or handling limits matter.

## Kinematic Bicycle Model

The bicycle model combines the front wheels and rear wheels into two virtual wheels. With wheelbase $L$, speed $v$, steering angle $\delta$, and heading $\theta$:

$$\dot{x}=v\cos\theta, \quad \dot{y}=v\sin\theta, \quad \dot{\theta}=\frac{v}{L}\tan\delta$$

This is the appropriate starting point for Sparky's Ackermann-like simulator and pure-pursuit controller.

## Ackermann and Differential Drive

Ackermann steering points front-wheel axes toward a common instantaneous center; controllers normally command a single equivalent steering angle. Differential drive turns by varying left and right wheel speeds and cannot directly use Ackermann steering equations.

## Validation

Define the reference point (`base_link`), wheelbase, steering bounds, speed bounds, integration step, and command units. Test straight motion, constant-radius turns, reverse motion if supported, and saturated steering. Model mismatch must be visible in documentation and metrics rather than silently compensated by gains.
