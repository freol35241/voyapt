import pytest
import numpy as np

from voyapt.weather import angle_difference, true_to_apparent_wind


def test_angle_difference():
    assert pytest.approx(-np.pi) == angle_difference(np.pi, 0)
    assert pytest.approx(np.pi) == angle_difference(0, np.pi)
    assert pytest.approx(np.pi) == angle_difference(0, 3 * np.pi)
    assert pytest.approx(np.pi) == angle_difference(-np.pi, 0)

    alphas = np.ones(1000) * np.pi
    betas = np.zeros_like(alphas)
    assert np.array_equal(-alphas, angle_difference(alphas, betas))


def test_true_to_apparent_wind():
    assert true_to_apparent_wind(10, np.pi / 2, 0, 0) == (10, np.pi / 2, np.pi / 2)
    assert true_to_apparent_wind(10, 3 / 2 * np.pi, 0, np.pi) == (
        10,
        3 / 2 * np.pi,
        np.pi / 2,
    )
    assert true_to_apparent_wind(10, 0, 10, 0) == (
        20,
        0,
        0,
    )
