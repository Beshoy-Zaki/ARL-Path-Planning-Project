# Autonomous Path Planning Algorithm

This project contains a Python implementation of a local path planning algorithm for an autonomous vehicle. The algorithm generates a drivable path based on detected cones that mark the boundaries of a track. It uses the vehicle's current pose (position and orientation) to compute a sequence of waypoints for the car to follow.

This implementation was developed as a solution for the FSAI-style path planning assignment.



---

## Quick Start

To run the simulation and test the algorithm, follow these steps.

### Prerequisites

* Python 3.9+

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv .venv

    # Activate on macOS/Linux
    source .venv/bin/activate

    # Activate on Windows
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running a Scenario

You can run any of the pre-built test scenarios using the command line.

```bash
python -m src.run --scenario <scenario_number>
```
For example, to run scenario 3:
```bash
python -m src.run --scenario 3
```

---

## Algorithm Overview

The core logic is implemented in `src/path_planning.py`. It uses a geometry-based approach that processes cone positions and outputs a sequence of 2D coordinates representing the planned path. The algorithm intelligently handles three distinct scenarios.

### 1. Both Track Boundaries Visible (Dual-Boundary Case)

When cones from both the left (blue) and right (yellow) sides of the track are visible, the algorithm aims to drive down the centerline.

* It pairs each blue cone with its nearest yellow neighbor.
* The **midpoint** of each pair becomes a waypoint on the path.
* This ensures the vehicle maintains an equal distance from both boundaries, creating a safe and stable path.

### 2. Single Track Boundary Visible

When only one side of the track is visible (e.g., only blue cones), the algorithm creates a parallel path using a perpendicular offset.

1.  It computes the direction vector between consecutive cones on the visible boundary.
2.  It calculates the perpendicular direction to this boundary line.
3.  It applies an **offset of 1.5 meters** to create a path that runs parallel to the cones.
    * If blue cones (left boundary) are visible, the path is offset to the **right**.
    * If yellow cones (right boundary) are visible, the path is offset to the **left**.

This creates an approximate centerline based on the assumption that the track has a consistent width.

### 3. No Cones Detected (Fallback)

When no cones are detected, the algorithm generates a simple, straight path along the vehicle's current heading (`yaw`). This ensures the car continues to move forward safely when sensor data is temporarily unavailable.

---

## ✨ Algorithm Characteristics

### Strengths

* **Computationally Efficient:** Requires only basic geometric calculations without needing complex optimization libraries.
* **Intuitive & Transparent:** The logic is easy to understand, making it great for learning and debugging.
* **Flexible & Robust:** Adapts well to varying numbers of detected cones and degrades gracefully when sensor information is limited.

### Limitations

* **Tight Curves:** The perpendicular offset method may not accurately represent the true centerline on very sharp turns.
* **Sensor Noise:** The algorithm does not filter for outlier cone detections, which could affect path quality.
* **Path Extension:** The linear extension at the end of the path does not account for potential upcoming turns beyond the last visible cone.

---

## 📜 Conclusion

This algorithm provides a simple, practical, and effective solution for the local path planning problem. By using straightforward geometric principles, it handles multiple real-world scenarios robustly. While it has limitations in highly complex situations, its simplicity and expandability make it an excellent foundation for more advanced autonomous navigation systems.
