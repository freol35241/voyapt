from typing import Union, Tuple

import numpy as np


def angle_difference(
    alpha: Union[float, np.ndarray], beta: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    return np.arctan2(np.sin(beta - alpha), np.cos(beta - alpha))


def apparent_to_true_wind(
    wind_speed: Union[float, np.ndarray],
    wind_direction: Union[float, np.ndarray],
    ship_speed: float,
    ship_heading: float,
):
    raise NotImplementedError


def true_to_apparent_wind(
    wind_speed: Union[float, np.ndarray],
    wind_direction: Union[float, np.ndarray],
    ship_speed: float,
    ship_heading: float,
) -> Tuple[
    Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]
]:

    u_s = ship_speed * np.sin(ship_heading)
    v_s = ship_speed * np.cos(ship_heading)

    u_w = wind_speed * np.sin(wind_direction)
    v_w = wind_speed * np.cos(wind_direction)

    u_tot = u_s + u_w
    v_tot = v_s + v_w

    aws = np.sqrt(u_tot ** 2 + v_tot ** 2)
    awd = (np.arctan2(-u_tot, -v_tot) - np.pi) % (2 * np.pi)
    awa = angle_difference(ship_heading, awd) % (2 * np.pi)

    return aws, awd, awa
