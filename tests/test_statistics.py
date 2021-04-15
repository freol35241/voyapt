import pytest
import numpy as np

from voyapt.statistics import (
    get_bin_midpoints,
    joint_probability_density_function,
    joint_probability_mass_function,
    monte_carlo,
)


def test_get_bin_midpoint():
    assert np.array_equal([1, 3, 5], get_bin_midpoints([0, 2, 4, 6]))


def test_joint_probability_mass_function_1d():
    pdf, edges = joint_probability_density_function(np.random.random_sample(10000))

    assert pdf * np.diff(edges) == pytest.approx(1.0)
    assert len(edges) == 1


def test_joint_probability_mass_function_2d():
    samples = np.random.random_sample(10000).reshape(-1, 2)
    pdf, edges = joint_probability_density_function(samples)

    assert pdf * np.diff(edges) == pytest.approx(1.0)
    assert len(edges) == 2


def test_joint_probability_mass_function_1d():
    pmf, edges = joint_probability_mass_function(np.random.random_sample(10000))

    assert pmf.sum() == pytest.approx(1.0)
    assert len(edges) == 1


def test_joint_probability_mass_function_2d():
    samples = np.random.random_sample(10000).reshape(-1, 2)
    pmf, edges = joint_probability_mass_function(samples)

    assert pmf.sum() == pytest.approx(1.0)
    assert len(edges) == 2


def test_monte_carlo_uniform():
    rng = np.random.default_rng()
    samples = rng.uniform(size=10)

    draws = monte_carlo(samples)

    assert len(draws) == 1e6
    assert set(draws) == set(samples)


def test_monte_carlo_probs():
    rng = np.random.default_rng()
    samples = rng.uniform(size=10)

    draws = monte_carlo(samples, probabilities=samples)

    assert len(draws) == 1e6
    assert set(draws) == set(samples)
