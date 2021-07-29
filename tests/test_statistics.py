from collections import Counter

import pytest
import numpy as np

from voyapt.statistics import (
    get_bin_midpoints,
    probability_density_function,
    probability_mass_function,
    pmf_reduce_to_univariate,
    monte_carlo,
)


def test_get_bin_midpoint():
    assert np.array_equal([1, 3, 5], get_bin_midpoints([0, 2, 4, 6]))


def test_probability_density_function_1d():
    pdf, edges = probability_density_function(np.random.random_sample(10000))

    assert (pdf * np.diff(edges)).sum() == pytest.approx(1.0)
    assert len(edges) == 1


def test_probability_density_function_2d():
    samples = np.random.random_sample(10000).reshape(-1, 2)
    pdf, edges = probability_density_function(samples)

    assert (
        pdf * np.outer(np.diff(edges[0]), np.diff(edges[1]))
    ).sum() == pytest.approx(1.0)
    assert len(edges) == 2


def test_probability_mass_function_1d():
    pmf, coords, edges = probability_mass_function(np.random.random_sample(10000))

    assert pmf.sum() == pytest.approx(1.0)
    assert len(coords) == 1
    assert len(edges) == 1


def test_probability_mass_function_2d():
    samples = np.random.random_sample(10000).reshape(-1, 2)
    pmf, coords, edges = probability_mass_function(samples)

    assert pmf.sum() == pytest.approx(1.0)
    assert len(coords) == 2
    assert len(edges) == 2


def test_pmf_reduce_to_univariate():
    samples = np.random.random_sample(10).reshape(-1, 2)
    pmf, coords, edges = probability_mass_function(samples)

    univariate_pmf, univariate_coords = pmf_reduce_to_univariate(
        pmf, coords, lambda x: np.sum(x, axis=1)
    )

    assert univariate_pmf.sum() == pytest.approx(1.0)
    assert (sorted(univariate_coords) == univariate_coords).all()


def test_monte_carlo_uniform():
    rng = np.random.default_rng()
    samples = rng.uniform(size=10)

    draws = monte_carlo(samples)

    assert len(draws) == 1e6
    assert set(draws) == set(samples)


def test_monte_carlo_probs():
    rng = np.random.default_rng()
    samples = rng.uniform(size=10)

    probs = samples / samples.sum()

    draws = monte_carlo(samples, probabilities=probs)

    assert len(draws) == 1e6
    assert set(draws) == set(samples)
    c = Counter(draws)
    for sample, prob in zip(samples, probs):
        assert c[sample] / 1e6 == pytest.approx(prob, rel=1e5)
