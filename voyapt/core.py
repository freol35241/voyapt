from typing import Generator

from voyapt import Waypoint, Leg, Route


def get_legs(route: Route) -> Generator[Leg, None, None]:
    for first, second in zip(route[:-1], route[1:]):
        yield Leg(first, second)


def leg_midpoint(leg: Leg) -> Waypoint:
    return leg.interpolate(0.5).to_geo_point()


def split_leg(leg: Leg, n: int = 10) -> Route:
    assert n >= 1, "n must be an integer in [1, inf)"

    step = 1.0 / n
    points = []

    for i in range(n + 1):
        points.append(leg.interpolate(i * step).to_geo_point())

    return points


def track_distance(route: Route) -> float:
    return sum(leg.track_distance() for leg in get_legs(route))


def merge_routes(*routes: Route) -> Route:
    out = []
    for route in routes:
        if out:
            assert (
                out[-1] == route[0]
            ), "Mismatch in last and first point in consecutive list of route!"
            out += route[1:]
        else:
            out += route

    return out
