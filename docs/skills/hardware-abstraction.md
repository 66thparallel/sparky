# Hardware Abstraction

## Purpose

A hardware abstraction layer (HAL) exposes a stable vehicle-facing interface while isolating drivers and transport details. The controller should request a bounded steering and speed command without needing to know whether the target is a simulator, CAN bus, or motor controller.

## Interface Design

Define clear command and state contracts, including units, valid ranges, timestamps, frame IDs, calibration assumptions, and fault reporting. Make commands explicit about their control mode; never overload one numeric field with multiple meanings.

## Simulator Parity

Implement the same high-level interface for simulation and hardware. Simulation adapters may model delay and saturation, but must not hide invalid commands that hardware would reject. This lets integration tests exercise the controller without hardware.

## Drivers and Safety

Drivers own device-specific communication, watchdogs, and error translation. The HAL must put the system in a safe state on stale commands, disconnects, or invalid state. Keep emergency-stop handling independent of normal planning logic.
