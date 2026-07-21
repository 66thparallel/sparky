# Feedforward Control

## Purpose

Feedforward predicts the command required for a desired state; feedback corrects the remaining error:

$$u = u_{ff} + u_{fb}$$

It reduces lag when the model and desired trajectory are known, but it cannot replace feedback because models and disturbances are imperfect.

## Examples

- Command throttle proportional to desired acceleration plus an offset for rolling resistance.
- Command steering from desired curvature: $\delta_{ff}=\arctan(L\kappa)$ for a bicycle model.
- Use desired velocity and acceleration from a trajectory rather than waiting for speed error to grow.

## Safe Use

Apply the same saturation and rate limits to the combined command. Verify units and sign conventions, then log feedforward and feedback terms separately. If a large feedback term is always required, improve the model or calibration instead of increasing gains blindly.
