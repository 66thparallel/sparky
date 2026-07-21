# State-Space Control

## Model Form

State-space models represent a system as:

$$\dot{x}=Ax+Bu, \qquad y=Cx+Du$$

where $x$ is the state, $u$ the input, and $y$ the measured output. Linearize nonlinear vehicle dynamics around a declared operating point before applying linear control methods.

## Common Designs

State feedback uses $u=-Kx$. LQR selects $K$ by balancing state error and control effort through cost matrices $Q$ and $R$. Observers, such as a Kalman filter, estimate unmeasured states when the system is observable.

## Engineering Guidance

State-space control is valuable when variables are coupled or constraints matter, but it requires a credible model, measurement assumptions, and validation. Discretize the model at the actual controller period, handle actuator saturation outside the linear design, and keep a safe fallback controller.

For Sparky, begin with validated kinematic tracking and introduce a state-space model only with a specific measured limitation to solve.
