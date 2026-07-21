# C++ Performance

## Measure First

Start with a correct, observable implementation, then profile representative workloads. Record latency distributions, allocations, CPU use, and missed deadlines; do not optimize based only on intuition.

## High-Value Practices

- Avoid unnecessary copies; pass large immutable data by `const` reference and move owned results.
- Reserve capacity for vectors used every control cycle.
- Reuse buffers and avoid heap allocation in deterministic hot paths.
- Prefer contiguous storage and data layouts that are read sequentially.
- Keep interfaces clear; do not trade correctness for micro-optimizations without evidence.

## Profiling

Use compiler warnings, sanitizers, `perf`, or a suitable profiler to find real hotspots. Build with optimization and debugging symbols when profiling. Validate numerical output and timing after each optimization because a faster incorrect controller is not useful.
