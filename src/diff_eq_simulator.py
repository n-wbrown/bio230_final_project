"""
diff_eq_simulator.py

Contains the code takes the differential equations for a system and generates
time series data with some stochasticity.
"""
import numpy as np

from .diff_eq_generator import create_callables


def example_function():
    print(f"the example function in {__file__} is running")


def simulate_network(rnet: "ReactionNetwork", x0: np.ndarray, t0: float,
                     tf:float, noise_intensity: np.ndarray | None=None,
                     num_steps: int=1000) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate the reaction network, produce time series data of the quantity of
    the reactants.

    Args: 
        rnet : The configured reaction network
        f: function describing system dynamics takes
        x0: Initial condition for the system
        t0: Start time
        tf: End time
        noise_intensity: Strength of the stochastic noise for each qty
        num_steps: Number of simulation steps

    Returns:
        reactants : 2d array of the reactant quantities at each time step.
        time: Array of time points
    """
    eqs = create_callables(
        species=rnet.species,
        odes=rnet.odes,
    ) 

    times = np.array([])

    def temp_func(X, t):
        return np.array([eq(*X) for eq in eqs])

    result, times = simulate_differential_equation(
        temp_func,
        x0=x0,
        t0=t0,
        tf=tf,
        noise_intensity=noise_intensity,
        num_steps=num_steps
    )

    return result, times


def simulate_differential_equation(f, x0: np.ndarray, t0: float, tf:float,
                                    noise_intensity: np.ndarray | None=None,
                                    num_steps: int=1000
                                    ) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate a system of differential equations with stochasticity.
    
    Args:
        f: list of functions describing system dynamics takes
        x0: Initial condition for the system
        t0: Start time
        tf: End time
        noise_intensity: Strength of the stochastic noise for each qty
        num_steps: Number of simulation steps

    Returns:
        x: Array of reactant quantities over time
        time: Array of time points
    """
    # Initialize time and state arrays
    state_size = x0.shape[0]

    has_noise = False
    if noise_intensity is not None:
        if np.any(noise_intensity > 0.0):
            has_noise = True

    time = np.linspace(t0, tf, num_steps)
    x = np.zeros((num_steps, len(x0)))
    x[0] = x0

    dt = time[1] - time[0]

    for i in range(1, num_steps):
        # Compute deterministic part (dx/dt = f(x,t))
        dx = f(x[i-1], time[i-1]) * dt

        # Add stochasticity (Gaussian noise if white noise is selected)
        if has_noise:
            noise = np.random.normal(size=state_size) * noise_intensity
            dx += noise

        # Update the state with the deterministic and stochastic parts
        x[i] = x[i-1] + dx

    return x, time
