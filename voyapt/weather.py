from typing import Sequence

import numpy as np
import xarray as xr

from voyapt import GeoPoint

def apparent_wind_at_point(ds: xr.Dataset, point: GeoPoint, speed: float, heading: float):
    pt = ds.sel(longitude=point.longitude_deg % 360, latitude=point.latitude_deg, method="nearest")
    
    heading %= (2*np.pi)

    u_s = speed*np.sin(heading)
    v_s = speed*np.cos(heading)

    u10 = pt.u10 - u_s
    v10 = pt.v10 - v_s

    aws = np.sqrt(u10**2 + v10**2)
    awd = (np.arctan2(u10, v10) - np.pi) % (2*np.pi)
    awa = np.arctan2(np.sin(awd-heading), np.cos(awd-heading)) % (2*np.pi)

    return awa, awd, aws

def true_wind_at_point(ds: xr.Dataset, point: GeoPoint, heading=0):
    twa, twd, tws = apparent_wind_at_point(ds=ds, point=point, speed=0, heading=heading)
    return twa, twd, tws

def joint_probability_distribution(speeds: Sequence[float], angles: Sequence[float], speed_edges=None, angle_edges=None):
    speed_edges = speed_edges or list(range(0, 25, 2))
    angle_edges = angle_edges or np.deg2rad(list(range(0, 361, 15)))

    assert len(speeds) == len(angles), "List inputs must be of same length!"
    samples, x_edges, y_edges = np.histogram2d(speeds, angles, bins=[speed_edges, angle_edges])
    probabilities = samples / len(speeds) * 100

    return probabilities, x_edges, y_edges

