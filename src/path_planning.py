from __future__ import annotations
from typing import List
import math

from src.models import CarPose, Cone, Path2D


class PathPlanning:
    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        car_x, car_y, car_yaw = self.car_pose.x, self.car_pose.y, self.car_pose.yaw
        path = []
        blue = [c for c in self.cones if c.color == 1]
        yellow = [c for c in self.cones if c.color == 0]

        # both visible use midpoints
        if blue and yellow:
            for b in blue:
                nearest_y = min(yellow, key=lambda y: (b.x - y.x)**2 + (b.y - y.y)**2)
                path.append(((b.x + nearest_y.x) / 2, (b.y + nearest_y.y) / 2))

        # if single one visible offset form it
        elif self.cones:
            cones = sorted(self.cones, key=lambda c: (c.x - car_x)**2 + (c.y - car_y)**2)
            for i, c in enumerate(cones):
                if i < len(cones) - 1:
                    next_c = cones[i + 1]
                    dx, dy = next_c.x - c.x, next_c.y - c.y
                else:
                    dx, dy = math.cos(car_yaw), math.sin(car_yaw)

                # perpendicular
                nx, ny = -dy, dx
                norm = math.hypot(nx, ny)
                nx /= norm
                ny /= norm

                # if blue shift right if yellow shift left
                sign = -1 if c.color == 1 else 1
                path.append((c.x + nx * 1.5 * sign, c.y + ny * 1.5 * sign))

        #if no cones go straight ahead
        else:
            for i in range(1, 10):
                path.append((car_x + math.cos(car_yaw) * i,
                             car_y + math.sin(car_yaw) * i))
        path.sort(key=lambda p: (p[0] - car_x)**2 + (p[1] - car_y)**2)
        path.insert(0, (car_x, car_y))

        if len(path) >= 2:
            dx, dy = path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]
            angle = math.atan2(dy, dx)
            for i in range(1, 6):
                path.append((path[-1][0] + math.cos(angle) * 0.5,
                             path[-1][1] + math.sin(angle) * 0.5))

        return path
