# Testing Robotics Software

## Test Pyramid

Use fast unit tests for geometry, control laws, and validation; integration tests for ROS node interfaces; simulation tests for closed-loop behavior; and regression tests for previously fixed failures. Each layer catches a different class of defect.

## Unit Tests

Use `gtest`/`gmock` for C++ and the standard Python test tooling for Python packages. Cover nominal behavior, boundary values, invalid input, saturation, angle wrapping, and stale-data behavior. Inject clocks and interfaces where possible for deterministic tests.

## Integration and Simulation

Start a minimal ROS graph, publish known inputs, and assert outputs, frame IDs, timestamps, and QoS behavior. Use fixed initial conditions and random seeds in simulation. Set explicit timeouts so tests fail with diagnostic information instead of hanging.

## Regression Evidence

Record test scenarios and metrics such as maximum cross-track error, completion time, and saturated-command count. Add a test whenever a production or simulation defect is fixed.
