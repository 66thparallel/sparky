# Robot Software Stack

## Layers

| Layer | Responsibility |
| --- | --- |
| Perception | Convert raw sensors to useful observations |
| Localization | Estimate vehicle pose and uncertainty |
| Mapping | Represent the environment |
| Planning | Choose a safe, feasible route or trajectory |
| Controls | Track desired motion within limits |
| Hardware | Execute commands and report state |

Each layer should state its inputs, outputs, frames, rates, uncertainty, and failure behavior. A layer must not silently compensate for an upstream contract violation.

## Current Sparky Scope

Sparky currently focuses on route publication, path tracking, vehicle simulation, TF, and metrics. Perception, localization, mapping, hardware drivers, and full safety supervision are future integration concerns. Keep interfaces extendable without pretending those missing layers already exist.
