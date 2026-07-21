# Robotics Math

## Linear Algebra

Vectors represent directions or states; matrices represent linear maps. Check dimensions and frame meaning before multiplying. Rotation matrices are orthonormal: $R^{-1}=R^T$.

## Rotations

Use rotation matrices for composition and quaternions for 3D orientation messages. A quaternion must be normalized and has a sign ambiguity: $q$ and $-q$ represent the same rotation. Avoid repeated Euler-angle conversion because it can cause singularities and convention mistakes.

## Homogeneous Transforms

Use homogeneous matrices to compose rotation and translation:

$$T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$$

Composition order matters. $T_{AC}=T_{AB}T_{BC}$ means transform from frame $C$ into frame $A$ through $B$. Label every transform with source and target frames.

## Numerical Practice

Use tolerances for floating-point comparison, reject non-finite inputs, and test identities, inverses, and known geometric cases. For runtime ROS transforms, TF2 should remain the system of record.
