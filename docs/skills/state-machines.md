# State Machines

## States

Use explicit states to make system behavior predictable:

| State | Meaning |
| --- | --- |
| Idle | Ready, no motion command requested |
| Planning | Producing or validating a route |
| Executing | Tracking a valid route |
| Recovery | Handling a recoverable fault or replan |
| Emergency stop | Motion inhibited until explicitly cleared |

## Transition Rules

For every transition, define the event, guards, entry action, exit action, timeout, and safe output. For example, `Executing → Recovery` may be triggered by a stale path, excessive tracking error, or missing odometry. Every unexpected event should have deterministic handling.

## Safety Principles

Emergency stop must override normal state transitions and command zero or an explicitly safe command. Avoid scattered Boolean flags that represent implicit state. Publish state and transition reasons so operators and tests can determine why a vehicle stopped.
