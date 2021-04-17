from functools import wraps, partial
from typing import Callable, Sequence

import numpy as np


def get_bin_midpoints(bin_edges):
    bin_edges = np.asarray(bin_edges)
    return 0.5 * (bin_edges[1:] + bin_edges[:-1])


@wraps(np.histogramdd)
def probability_density_function(*args, **kwargs):
    if not kwargs.get("density", True) or not kwargs.get("normed", True):
        raise ValueError(
            "Not possible to calculate probability density function when"
            " 'density' or 'normed' is set to False"
        )
    kwargs.update({"density": True})
    return np.histogramdd(*args, **kwargs)


@wraps(np.histogramdd)
def probability_mass_function(*args, **kwargs):
    if kwargs.get("density") or kwargs.get("normed"):
        raise ValueError(
            "Not possible to calculate probability mass function when"
            " 'density' or 'normed' is set to True"
        )
    hist, edges = np.histogramdd(*args, **kwargs)
    return hist / hist.sum(), [get_bin_midpoints(bins) for bins in edges], edges


def pmf_reduce_to_univariate(pmf: np.ndarray, coords: np.ndarray, reducer: Callable):
    assert pmf.shape == tuple(
        [len(crds) for crds in coords]
    ), "Dimensions of pmf and provided coords must agree!"

    indices = np.array(list(np.ndindex(pmf.shape)))
    combos = np.array([pts[ixs] for pts, ixs in zip(coords, indices.T)]).T

    pts: np.ndarray = reducer(combos)

    pmf = pmf.flatten()

    assert len(pmf) == len(
        pts
    ), "Reducer function did not return data in proper format!"

    sorted_ixs = pts.argsort()
    return pmf[sorted_ixs], pts[sorted_ixs]


def monte_carlo(
    samples: Sequence, probabilities: Sequence = None, iterations=1e6
) -> np.ndarray:
    probabilities = (
        np.ones(len(samples)) if probabilities is None else np.array(probabilities)
    )
    drawn_indices = np.random.default_rng().choice(
        len(samples), size=int(iterations), p=probabilities / probabilities.sum()
    )

    return samples[drawn_indices]
