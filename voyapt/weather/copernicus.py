import numpy as np
import xarray as xr

from voyapt import Waypoint

open_mfdataset = xr.open_mfdataset


def vectors_to_true_wind(
    dataset: xr.Dataset, east_label="u10", north_label="v10"
) -> xr.Dataset:
    u10 = dataset[east_label]
    v10 = dataset[north_label]

    tws = np.sqrt(u10 ** 2 + v10 ** 2)
    twd = (np.arctan2(u10, v10) - np.pi) % (2 * np.pi)

    return dataset.assign(variables={"tws": tws, "twd": twd})


def point_data(dataset: xr.Dataset, waypoint: Waypoint, time=None) -> xr.Dataset:

    selection = {
        "longitude": waypoint.longitude_deg % 360,
        "latitude": waypoint.latitude_deg,
        "method": "nearest",
    }

    if time:
        selection["time"] = time

    return dataset.sel(**selection)
