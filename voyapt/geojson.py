from typing import Any, List
from copy import deepcopy

from geojson import (
    Point,
    LineString,
    Feature,
    FeatureCollection,
    dumps,
    dump,
    loads,
    load,
)

from voyapt import Waypoint, Leg, Route
from voyapt.core import get_legs


def waypoint_to_geojson(wp: Waypoint, properties: dict = None) -> Feature:
    props = deepcopy(properties or dict())
    props.update({"voyapt_type": "Waypoint"})
    return Feature(
        geometry=Point(
            wp.latlon_deg[:2][::-1]
        ),  # Flipping to comply with GeoJSON (lon, lat) definition
        properties=props,
    )


def leg_to_geojson(leg: Leg, properties: dict = None) -> LineString:
    props = deepcopy(properties or dict())
    props.update({"voyapt_type": "Leg"})
    wps = leg.geo_points()
    return Feature(
        geometry=LineString([wps[0].latlon_deg[:2][::-1], wps[1].latlon_deg[:2][::-1]]),
        properties=props,
    )


def route_to_geojson(
    route: Route,
    properties: dict = None,
    wp_properties: List[dict] = None,
    leg_properties: List[dict] = None,
) -> FeatureCollection:

    # First wps
    wp_features = []
    wp_properties = wp_properties or [{}] * len(route)
    for ix, (wp, props) in enumerate(zip(route, wp_properties)):
        props.update({"index": ix + 1})
        wp_features.append(waypoint_to_geojson(wp, properties=props))

    # then legs
    leg_features = []
    leg_properties = leg_properties or [{}] * (len(route) - 1)
    for ix, (leg, props) in enumerate(zip(get_legs(route), leg_properties)):
        props.update({"index": ix + 1})
        leg_features.append(leg_to_geojson(leg, properties=props))

    properties = properties or dict()
    properties.update({"voyapt_type": "Route"})

    return FeatureCollection(features=wp_features + leg_features, **properties)
