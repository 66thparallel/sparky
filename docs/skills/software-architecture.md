# Software Architecture

## Layer the System

Separate transport, domain logic, and infrastructure. ROS callbacks should translate messages into domain inputs; planning and control logic should be testable without a running ROS graph; adapters should publish results and access external resources.

## Interfaces and Dependencies

Depend on small, stable interfaces rather than concrete implementations. Inject dependencies such as clocks, vehicle state sources, and command sinks into domain components so tests can replace them with fakes. Avoid cyclic package dependencies.

## Plugin Architecture

Use plugins when multiple implementations must be selected at runtime, such as planners or controllers with the same contract. Keep the interface narrow, define configuration and failure behavior, and provide a known-safe default. Do not add plugins merely to avoid a simple conditional.

## Sparky Direction

The current planner → controller → simulator pipeline is a good layered baseline. Keep topic contracts stable while evolving algorithms internally; publish metrics at component boundaries to make integration behavior visible.
