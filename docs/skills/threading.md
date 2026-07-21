# C++ Threading

## Start Simple

Prefer single-threaded execution until parallelism solves a measured responsiveness or throughput problem. Shared mutable state is a source of timing-dependent defects.

## Synchronization

Use `std::mutex` with `std::lock_guard` or `std::unique_lock` to protect a clear ownership boundary. Use `std::condition_variable` for waiting on a state predicate, always checking that predicate in a loop. Use atomics only for simple independent values with understood memory ordering.

## Real-Time Concerns

Never hold a lock while performing blocking I/O or invoking unknown callbacks. Keep critical sections short and use a documented lock order to prevent deadlocks. Priority inversion occurs when a high-priority task waits on a lock held by a lower-priority task; reduce shared locks in high-rate control code.

Lock-free structures can avoid blocking but are complex and are not automatically faster. Choose them only when profiling and correctness requirements justify their added difficulty.
