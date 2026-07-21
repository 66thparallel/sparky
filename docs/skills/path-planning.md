# Path Planning

## Plan at the Right Level

A path answers *where* the vehicle should travel. A trajectory also specifies *when* it should be at each state. Keep route planning, path smoothing, and time parameterization separate so each can be tested independently.

## Grid-Based Search

Occupancy grids discretize free and occupied space. Breadth-first search finds minimum-hop paths in unweighted grids. Dijkstra finds a minimum-cost path for non-negative edge costs. A* uses the same guarantee when its heuristic never overestimates the remaining cost:

$$f(n) = g(n) + h(n)$$

For a 2D grid, Euclidean or Manhattan distance is a useful admissible heuristic when it matches permitted motion.

## Vehicle-Aware Planning

Standard grid paths ignore steering limits. Hybrid A* searches poses $(x, y, \theta)$ using feasible vehicle motion primitives. State lattices precompute feasible primitives and can enforce curvature and direction constraints. Both are more suitable for Ackermann vehicles than plain A* when maneuverability matters.

## Sparky Guidance

The current planner publishes parameter-defined waypoints. Retain `nav_msgs/Path` as the path contract, then add obstacle inputs and a planner behind that interface. Define map resolution, obstacle inflation, vehicle footprint, goal tolerance, and failure behavior before selecting an algorithm.
