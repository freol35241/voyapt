import pytest

from voyapt import (
    Waypoint,
    Leg,
    Route,
)
from voyapt.core import (
    get_legs,
    leg_midpoint,
    split_leg,
    track_distance,
    merge_routes,
)


def test_get_legs():
    wp1 = Waypoint(latitude=56, longitude=11)
    wp2 = Waypoint(latitude=57, longitude=12)
    wp3 = Waypoint(latitude=58, longitude=13)
    route = [wp1, wp2, wp3]

    legs = list(get_legs(route))

    assert len(legs) == 2
    assert legs[0].geo_points()[0] == wp1
    assert legs[0].geo_points()[1] == wp2
    assert legs[1].geo_points()[0] == wp2
    assert legs[1].geo_points()[1] == wp3


def test_leg_midpoint():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    leg = Leg(wp1, wp2)

    assert isinstance(leg_midpoint(leg), Waypoint)


def test_split_leg():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    leg = Leg(wp1, wp2)

    route = split_leg(leg, n=10)

    assert len(route) == 11  # 10 legs -> 11 Waypoints

    with pytest.raises(AssertionError):
        split_leg(leg, n=-20)

    with pytest.raises(TypeError):
        split_leg(leg, n=5.5)


def test_track_distance():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    wp3 = Waypoint(latitude=58, longitude=13, degrees=True)
    route = [wp1, wp2, wp3]

    dist = track_distance(route)

    assert isinstance(dist, float)
    assert dist > 0.0


def test_merge_routes():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    wp3 = Waypoint(latitude=58, longitude=13, degrees=True)
    route1 = [wp1, wp2]
    route2 = [wp2, wp3]

    route3 = merge_routes(route1, route2)

    assert route3[:2] == route1
    assert route3[1:] == route2

    with pytest.raises(AssertionError):
        merge_routes(route1, list(reversed(route2)))

    assert len(merge_routes()) == 0  # No inputs should give empty list in return
