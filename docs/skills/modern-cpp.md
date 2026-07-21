# Modern C++

## Ownership and RAII

Use automatic storage duration by default. RAII ties a resource's lifetime to an object's lifetime, so locks, files, and ROS handles are released even when errors occur. Use `std::unique_ptr` for exclusive ownership and `std::shared_ptr` only where ownership is genuinely shared; avoid owning raw pointers.

## Value Semantics

Prefer returning values. Copy when an independent value is needed; move when transferring resources from an expiring object. Accept read-only inputs as `const T&` unless small-value passing is clearer.

## Language Features

- Use `constexpr` for values and functions that can be computed at compile time.
- Use structured bindings to make tuple-like results readable.
- Mark overrides with `override`; use `enum class` for scoped types.
- Prefer standard-library algorithms and containers over manual memory management.

## ROS 2 Note

ROS 2 APIs may use shared pointers for message delivery. Follow their required callback signatures, but do not propagate shared ownership into unrelated domain code without need.
