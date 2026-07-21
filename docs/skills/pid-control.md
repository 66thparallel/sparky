# PID Control

## Controller Law

A PID controller combines present, accumulated, and changing error:

$$u(t)=K_p e(t)+K_i\int e(t)\,dt+K_d\frac{de(t)}{dt}$$

Use it for a well-defined scalar error, such as speed error, steering-actuator error, or heading correction. A PID loop alone is not a path-following algorithm; it needs a geometric error signal.

## Discrete Implementation

Use measured elapsed time $dt$, not an assumed fixed period. Initialize derivative state on the first sample, guard against zero or unusually large $dt$, and filter derivative terms when measurements are noisy.

## Saturation and Windup

Clamp output to actuator limits. Prevent integral windup by clamping the integral, back-calculating from saturation, or pausing integration when further error would push an already saturated output outward.

## Tuning Order

Set $K_i=K_d=0$, increase $K_p$ until response is sufficiently quick without sustained oscillation, add $K_d$ for damping, then add only enough $K_i$ to remove persistent bias. Re-test at representative speeds and loop periods.
