"""
diff_eq_recreator.py

Tools for recreating the differential equation from the time series data
"""
import numpy as np
import pysr

from src.diff_eq_simulator import (simulate_network)

def example_function():
    print(f"the example function in {__file__} is running")


def rand_runner(rnet: ".diff_eq_generator.ReactionNetwork",
                ubound: np.ndarray,
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
    for _ in range(runs):
        reactants, times = simulate_network(
            rnet,
            x0=ubound * np.random.random(ubound.shape),
            t0=0,
            tf=1,
            num_steps=50,
            noise_intensity=np.array([1e-3]*3)
        )
        reactants_data.append(reactants)
        times_data.append(times)

    return reactants_data, times_data


def regressor_fit(dataset: np.ndarray, target: np.ndarray
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
        maxsize=15,
        populations=4,
        niterations=40,  # < Increase me for better results
        binary_operators=["+", "*"],
        unary_operators=[
            "cos",
            "exp",
            "sin",
            "inv(x) = 1/x",
            # ^ Custom operator (julia syntax)
        ],
        extra_sympy_mappings={"inv": lambda x: 1 / x},
        # ^ Define operator for SymPy as well
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",
        # ^ Custom loss function (julia syntax)
        # warm_start=True,
        verbosity=0,
    )
    model.fit(
        dataset,
        target,
    )

    return model
