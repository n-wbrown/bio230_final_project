"""
utils.py

A collection of misc. tools.
"""

import numpy as np


def derivative_finder_diff(reactants_data: np.ndarray, times_data: np.ndarray) -> np.ndarray:
    """
    Simple difference-based differentiator.

    Args:
        reactants_data: 2d array [t,q] of any quantity that evolves w/ time.
        times_data: 1d array of the timestamps of reactants_data.
    Returns:
        result: 2d array [t, dq/dt] of the 1st derivative of the quantity wrt time.
    """
    return (
        np.diff(reactants_data, axis=0) /
        np.repeat(
            np.diff(times_data)[:, np.newaxis],
            repeats=reactants_data.shape[1],
            axis=1,
        )
    )

def lotka_volterra(
    X: np.ndarray,
    t: float,
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 1.0,
    delta: float = 1.0,
) -> np.ndarray:
    """
    Implemenation of the lotka-volterra model. Intended for testing.

    Args:
        X: 1d, len=2, array of the respective populations
        t: current time (not used)
        alpha: parameter (see wikipedia page)
        beta: parameter (see wikipedia page)
        gamma: parameter (see wikipedia page)
        delta: parameter (see wikipedia page)

    Returns:
        result: Numpy array of derivatives, element-wise matched with X

    """
    return np.array(
        [
            alpha * X[0] - beta * X[0] * X[1],
            -1 * gamma * X[1] + delta * X[0] * X[1],
        ]
    )
