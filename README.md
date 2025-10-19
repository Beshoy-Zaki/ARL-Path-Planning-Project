# Path Planning Algorithm for Autonomous Driving

## Introduction

In this document, I am going to discuss the algorithm I implemented in `src/path_planning.py` for autonomous vehicle navigation. The algorithm generates a drivable path based on detected cones marking the track boundaries, using the vehicle's current position and orientation to compute waypoints the car can follow.

---

## Algorithm Overview

The `PathPlanning` class implements a geometry-based approach that processes cone positions and outputs a sequence of 2D coordinates representing the planned path. The algorithm handles three distinct scenarios: both track boundaries visible, a single boundary visible, or no cones detected.

### Input Requirements

-   **Vehicle State:** Current position $(x, y)$ and orientation (yaw angle).
-   **Cone Data:** A list of cone objects containing position coordinates $(x, y)$ and a color identifier (1 for blue, 0 for yellow).

### Output Format

The algorithm returns a `Path2D` object consisting of ordered $(x, y)$ coordinate pairs that define the trajectory.

---

## Implementation Logic

### Cone Separation

The algorithm begins by categorizing cones by color into separate lists. This separation is essential because blue and yellow cones represent opposite track boundaries, and the path should generally follow the centerline between them.

### Dual-Boundary Case

When cones from both sides are visible, the algorithm pairs each blue cone with its nearest yellow neighbor. The midpoint of each pair becomes a waypoint on the path. This approach ensures the vehicle drives through the center of the track, maintaining equal distance from both boundaries.

### Single-Boundary Case

When only one boundary is visible, the algorithm employs a perpendicular offset strategy. Cones are first sorted by distance from the vehicle. For each consecutive pair of cones, the algorithm:

1.  Computes the direction vector between them.
2.  Calculates the perpendicular direction.
3.  Applies an offset of 1.5 units perpendicular to the cone line.

The offset direction depends on which boundary is visible. For blue cones (left boundary), the path shifts right; for yellow cones (right boundary), the path shifts left. This creates an approximate centerline based on the assumption that the track has a consistent width.

### No-Cone Fallback

When no cones are detected, the algorithm generates a straight path along the vehicle's current heading. Ten waypoints are placed at unit intervals in the direction defined by the yaw angle.

---

## Path Refinement

The final stage includes two operations:

-   **Sorting:** Waypoints are ordered by distance from the vehicle to ensure the path progresses logically forward.
-   **Extension:** I searched and found out that extending the path beyond the last cone provides continuous path information even as the vehicle approaches the last visible cone. This is done by computing the direction vector between the final two points and adding five additional waypoints at 0.5 unit intervals.

### Handling Edge Cases

The algorithm includes specific logic for scenarios where three or more cones appear on a single side. Instead of treating this as an error condition, it processes these cones sequentially, creating offset waypoints for each segment. This makes the path more stable when cone distribution is asymmetric.

---

## Algorithm Characteristics

### Strengths

-   The implementation is computationally efficient, requiring only basic geometric calculations without complex optimization or external libraries.
-   The logic is transparent and follows intuitive principles, making it suitable for educational purposes.
-   The algorithm adapts flexibly to varying sensor inputs and degrades gracefully when information is limited.

### Limitations

-   The perpendicular offset method may not accurately represent the true centerline on tight curves, where the track geometry is more complex.
-   The algorithm does not incorporate sensor noise filtering, so outlier cone detections can affect path quality.
-   When both boundaries are visible, the vehicle's heading is not used to anticipate path curvature.
-   The linear extension at the path's end does not account for potential upcoming turns.

---

## Conclusion

The implemented algorithm provides a practical solution for path planning in autonomous cars. It balances simplicity with effectiveness, using straightforward geometric principles to handle multiple scenarios. While the approach has limitations in complex situations, I think its merit is being really simple and expandable.
