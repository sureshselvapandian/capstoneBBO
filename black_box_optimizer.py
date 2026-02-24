"""Core utilities for sequential black-box optimisation with a GP surrogate.

This module provides a lightweight Expected Improvement workflow:
1) fit a Gaussian Process on observed data,
2) score random candidates with EI,
3) propose the highest-EI point.
"""

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from scipy.stats import norm


def _expected_improvement(x, model, inputs, outputs, xi=0.01):
    """Compute Expected Improvement (EI) at a single candidate point.

    Args:
        x: Candidate input vector with shape (d,).
        model: Fitted GaussianProcessRegressor.
        inputs: Observed inputs (unused directly, kept for API consistency).
        outputs: Observed objective values used to determine the current best.
        xi: Exploration offset; larger values encourage more exploration.

    Returns:
        Scalar EI value for the candidate point.
    """
    x = x.reshape(1, -1)
    mu, sigma = model.predict(x, return_std=True)
    sigma = sigma.reshape(-1, 1)

    best = np.max(outputs)

    with np.errstate(divide="warn"):
        Z = (mu - best - xi) / sigma
        ei = (mu - best - xi) * norm.cdf(Z) + sigma * norm.pdf(Z)
        ei[sigma == 0.0] = 0.0

    return ei[0, 0]


def _propose_next_point(model, inputs, outputs, dim, rng, n_candidates=5000):
    """Propose the next query by random-searching for maximum EI.

    Args:
        model: Fitted GaussianProcessRegressor.
        inputs: Observed inputs used by EI helper.
        outputs: Observed objective values used by EI helper.
        dim: Input dimensionality.
        rng: NumPy random generator for candidate sampling.
        n_candidates: Number of random candidates to evaluate.

    Returns:
        Best candidate found, clipped to [0, 1] and rounded to 6 decimals.
    """
    best_x = None
    best_ei = -np.inf

    for _ in range(n_candidates):
        x = rng.uniform(0.0, 1.0, size=(dim,))
        ei = _expected_improvement(x, model, inputs, outputs)
        if ei > best_ei:
            best_ei = ei
            best_x = x

    return np.round(np.clip(best_x, 0.0, 1.0), 6)


def optimise_black_box(
    initial_inputs,
    initial_outputs,
    max_queries,
    seed=0,
):
    """Run iterative GP-based proposal steps for black-box optimisation.

    This function fits a GP at each iteration and prints one proposed query
    point. It does not evaluate the true objective internally and therefore
    returns the original copied input/output arrays unchanged.

    Args:
        initial_inputs: Initial design matrix with shape (n_samples, n_features).
        initial_outputs: Initial objective values with shape (n_samples,).
        max_queries: Number of proposal iterations to run.
        seed: Random seed for reproducible candidate sampling.

    Returns:
        Tuple (inputs, outputs) as float NumPy arrays.
    """
    rng = np.random.default_rng(seed)

    inputs = initial_inputs.astype(float).copy()
    outputs = initial_outputs.astype(float).copy()
    dim = inputs.shape[1]

    for it in range(max_queries):
        kernel = Matern(nu=2.5)
        gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, normalize_y=True)
        gp.fit(inputs, outputs)

        x_next = _propose_next_point(gp, inputs, outputs, dim, rng)

        print(f"Iter {it+1}: x={x_next}")

    return inputs, outputs
