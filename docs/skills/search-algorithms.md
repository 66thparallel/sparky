# Search Algorithms

## Core Algorithms

| Algorithm | Complete | Optimal | Typical use |
| --- | --- | --- | --- |
| BFS | Yes on finite graphs | Yes for equal edge cost | Unweighted reachability |
| DFS | Yes with finite visited set | No | Exploration and connectivity |
| Dijkstra | Yes | Yes for non-negative costs | Cost-aware shortest path |
| A* | Yes | Yes with admissible, consistent heuristic | Goal-directed shortest path |

## Correct Implementation

Maintain a visited or closed set to prevent repeated work. In weighted search, store the best known cost $g(n)$ and ignore stale priority-queue entries. Define valid neighbors, boundary handling, obstacle checks, and path reconstruction before optimizing.

## A* Heuristics

An admissible heuristic satisfies $h(n) \leq h^*(n)$ and never overestimates remaining cost. A consistent heuristic also satisfies $h(n) \leq c(n,n') + h(n')$, which simplifies closed-set handling. The heuristic must reflect the motion model; a grid-distance heuristic does not capture steering constraints.
