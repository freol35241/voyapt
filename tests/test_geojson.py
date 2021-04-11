import pytest

from geojson import Point, LineString, FeatureCollection

from voyapt import Waypoint, Leg, Route
from voyapt.geojson import to_geojson


def test_to_geojson_unknown_type():
    with pytest.raises(RuntimeError):
        to_geojson(4)


def test_properties():
    wp = Waypoint(latitude=56, longitude=11, degrees=True)
    props = {"a": 1, "b": 2}

    feat = to_geojson(wp, properties=props)

    assert len(props.keys()) == 2
    assert props.items() <= feat["properties"].items()


def test_to_geojson_waypoint():
    wp = Waypoint(latitude=56, longitude=11, degrees=True)

    feat = to_geojson(wp)
    pt = feat["geometry"]

    assert feat["properties"]["voyapt_type"] == "Waypoint"
    assert isinstance(pt, Point)
    assert Waypoint(*pt["coordinates"][::-1], degrees=True) == wp


def test_to_geojson_leg():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    leg = Leg(wp1, wp2)

    feat = to_geojson(leg)
    linestring = feat["geometry"]

    assert feat["properties"]["voyapt_type"] == "Leg"
    assert isinstance(linestring, LineString)
    reconstructed = Leg(
        *[Waypoint(*pt[::-1], degrees=True) for pt in linestring["coordinates"]]
    )
    assert all(
        first == second
        for first, second in zip(leg.geo_points(), reconstructed.geo_points())
    )


def test_to_geojson_route():
    wp1 = Waypoint(latitude=56, longitude=11, degrees=True)
    wp2 = Waypoint(latitude=57, longitude=12, degrees=True)
    wp3 = Waypoint(latitude=58, longitude=13, degrees=True)
    route = [wp1, wp2, wp3]

    collection = to_geojson(route)

    assert isinstance(collection, FeatureCollection)
    assert collection["voyapt_type"] == "Route"
    assert len(collection["features"]) == 5
    assert (
        len(
            [
                feat
                for feat in collection["features"]
                if feat["geometry"]["type"] == "Point"
            ]
        )
        == 3
    )
    assert (
        len(
            [
                feat
                for feat in collection["features"]
                if feat["geometry"]["type"] == "LineString"
            ]
        )
        == 2
    )
