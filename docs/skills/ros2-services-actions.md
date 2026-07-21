# ROS 2 Services and Actions

## Choose the Right Interface

| Interface | Use it for | Avoid it for |
| --- | --- | --- |
| Topic | Continuous state or events | Request/response workflows |
| Service | Short, synchronous operations | Long-running or cancelable work |
| Action | Long-running goals with feedback and cancellation | Simple state streams |

## Services

Services have one request and one response. Examples include resetting the simulator, loading a route, or querying a component's configuration. Make handlers fast, validate input, and report success plus a useful failure reason.

## Actions

Actions provide a goal, periodic feedback, a final result, and cancellation. Use them for work such as planning to a destination, executing a route, or calibration. An action server must check cancellation regularly and publish meaningful feedback such as planning progress or remaining distance.

## Sparky Guidance

Route publication remains a topic. A future route-planning request should be an action if it may take noticeable time or needs cancellation; a `reset_simulation` operation is a service. Do not use a service to repeatedly transmit vehicle commands.
