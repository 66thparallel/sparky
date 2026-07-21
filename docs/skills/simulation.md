# Simulation

## Purpose and Scope

Simulation supports fast, repeatable validation before hardware testing. Document the model's intended fidelity: Sparky currently uses a kinematic bicycle simulator, so it is suitable for planner and tracker behavior, not tire-limit validation.

## Physics Assumptions

State the wheelbase, steering and speed limits, integration method, update period, initial pose, collision assumptions, and whether reverse is allowed. Keep command units consistent with the controller and publish odometry plus TF from the same simulated state.

## Noise and Time

Add sensor noise, delay, and actuation limits only when tests need them; use fixed seeds for reproducibility. Use ROS time consistently, and ensure simulated timestamps are monotonically increasing. Controllers should tolerate realistic message delay and stale-data timeouts.

## Test Scenarios

Include straight paths, constant-radius turns, sharp turns, path completion, invalid inputs, and reset behavior. Compare recorded tracking error and command saturation across changes. Simulation passing is necessary evidence, not proof that hardware will behave identically.
