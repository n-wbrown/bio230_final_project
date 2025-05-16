"""
diff_eq_recreator.py

Tools for recreating the differential equation from the time series data
"""
import numpy as np
import pysr

from src.diff_eq_simulator import (simulate_network)
from .utils import derivative_finder_diff

def example_function():
    print(f"the example function in {__file__} is running")


def rand_runner(rnet: ".diff_eq_generator.ReactionNetwork",
                ubound: np.ndarray|None = None, steps: int = 50,
                noise_intensity: np.ndarray|None = None,
                run_duration: int = 1,
                runs: int = 3) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """
    Take in a ReactionNetwork and run a set of randomized, simulated runs.

    Args: 
        rnet: The ReactionNetwork to be simulated
        ubound: Initial values for the reactants will be randomly selected
                between 0 and the values provided here
        runs: Number of independent simulations to execute
    Returns:
        reactants_data: a list of the reactant quantites over time for each sim 
        times_data: a list of the timestamps for each sim

    """
    reactants_data = []
    times_data = [] 

    _noise_intensity = np.zeros(len(rnet.species))
    if noise_intensity is not None:
        _noise_intensity = noise_intensity

    _ubound = np.ones(shape=(len(rnet.species)))
    if ubound is not None:
        _ubound = ubound

    for _ in range(runs):
        reactants, times = simulate_network(
            rnet,
            x0=_ubound * np.random.random(_ubound.shape),
            t0=0,
            tf=run_duration,
            num_steps=steps,
            noise_intensity=_noise_intensity,
        )
        reactants_data.append(reactants)
        times_data.append(times)

    return reactants_data, times_data

def data_set_bundler(qty_data: list[np.ndarray], times_data: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Take the output of rand_runner, calculate the derivatives and reformat the
    data to feed directly into pysr's fit method.

    Args:
        qty_data: A collections of runs over the same network
        times_data: The time stamps associated with each simulated run

    Returns:
        merged_qty_data: A 2d array of reactant quantites, appended in time
        merged_times_data: A 1d array of timestamps
        merged_qty_drv: A 2d array of the derivative of the reactant quantities.
    """
    qty_drv = []
    for qty, times in zip(qty_data, times_data):
        qty_drv.append(
            derivative_finder_diff(qty, times)
        )

    merged_qty_data = np.concat([qty[:-1,:] for qty in qty_data], axis=0)
    merged_times_data = np.concat([times[:-1] for times in times_data], axis=0)
    merged_qty_drv = np.concat(qty_drv, axis=0)

    return (
        merged_qty_data,
        merged_times_data,
        merged_qty_drv,
    )

def regressor_fit(dataset: np.ndarray, target: np.ndarray, maxsize: int = 20,
                  niterations: int = 40, verbosity: int = 0
                  ) -> "pysr.PySRRegressor":
    """
    Use pysr to fit the dataset and target.

    Args:
        dataset : 2d array with the reactant qty. time [t,q]
        target : 1d array containing the desired values, matched in t

    Returns:
        mode : fitted regressor model containing results
    """
    model = pysr.PySRRegressor(
        maxsize=maxsize,
        # populations=4,
        niterations=niterations,  # < Increase me for better results
        binary_operators=["+", "*"],
        # unary_operators=[
        #     "cos",
        #     "exp",
        #     "sin",
        #     "inv(x) = 1/x",
        #     # ^ Custom operator (julia syntax)
        # ],
        # extra_sympy_mappings={"inv": lambda x: 1 / x},
        # ^ Define operator for SymPy as well
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",
        # ^ Custom loss function (julia syntax)
        # warm_start=True,
        annealing=True,
        verbosity=verbosity,
    )
    model.fit(
        dataset,
        target,
    )

    return model
