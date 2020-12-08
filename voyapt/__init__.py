from typing import List, Generator

import nvector as nv
from nvector import GeoPoint, GeoPath, great_circle_distance

def points_equal(pt1: GeoPoint, pt2: GeoPoint) -> bool:
    return pt1.latlon == pt2.latlon

def legs(points: List[GeoPoint]) -> Generator[GeoPath]:

    for first, second in zip(points[:-1], points[1:]):
        yield GeoPath(first, second)

def midpoint(leg: GeoPath) -> GeoPoint:
    return leg.interpolate(0.5).to_geo_point()

def split(leg: GeoPath, n: int=10) -> List[GeoPoint]:
        assert n >= 1, "n must be an integer in [1, inf)"

        step = 1.0 / n
        points = []

        for i in range(n + 1):
            points.append(
                leg.interpolate(i*step).to_geo_point()
            )

        return points

def track_distance(points: List[GeoPoint]) -> float:
    return sum(leg.track_distance() for leg in legs(points))

def merge(points1: List[GeoPoint], points2: List[GeoPoint]) -> List[GeoPoint]:
    assert points_equal(points1[-1], points2[0]), "Last point in first list and first point in second list must be equal!"
    return points1 + points2[1:]