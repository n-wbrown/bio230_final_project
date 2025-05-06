"""
diff_eq_recreator.py

Tools for recreating the differential equation from the time series data
"""
import numpy as np
import pysr


def example_function():
    print(f"the example function in {__file__} is running")




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
