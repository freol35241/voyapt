from typing import Callable, List

import numpy as np

from voyapt import Waypoint, Leg, Route
from voyapt.core import leg_midpoint, get_legs


def joint_probability_distribution(
    speeds: Sequence[float], angles: Sequence[float], speed_edges=None, angle_edges=None
):
    speed_edges = speed_edges or list(range(0, 25, 2))
    angle_edges = angle_edges or np.deg2rad(list(range(0, 361, 15)))

    assert len(speeds) == len(angles), "List inputs must be of same length!"
    samples, x_edges, y_edges = np.histogram2d(
        speeds, angles, bins=[speed_edges, angle_edges]
    )
    probabilities = samples / len(speeds) * 100

    return probabilities, x_edges, y_edges


class DiscreateDistribution:
    def __init__(self, probabilities: np.ndarray, *edges: np.ndarray):
        self._probabilities = probabilities
        self._edges = edges

    @classmethod
    def from_samples(cls, samples: np.ndarray, *bins: np.ndarray):
        bins = bins or None
        probs, edges = np.histogramdd(samples, bins=bins)
        probs /= probs.sum()
        return cls(probs, *edges)

    @property
    def dimensionality(self):
        return len(self._edges)

    def bin_edges(self) -> List[np.ndarray]:
        return self._edges

    def bin_midpoints(self) -> List[np.ndarray]:
        return [0.5 * (edge[1:] + edge[:-1]) for edge in self._edges]

    def probabilities(self) -> np.ndarray:
        return self._probabilities


def monte_carlo(
    func: Callable, distribution: DiscreateDistribution, iterations=1e6
) -> np.ndarray:
    pass