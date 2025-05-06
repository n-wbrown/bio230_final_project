"""
diff_eq_simulator.py

Contains the code takes the differential equations for a system and generates
time series data with some stochasticity.
"""
import numpy as np

# from  diff_eq_generator import ReactionNetwork


def example_function():
    print(f"the example function in {__file__} is running")


def simulate_network(rnet: "ReactionNetwork", initial: np.ndarray,
                     times: np.ndarray) -> np.ndarray:
    """
    Simulate the reaction network, produce time series data of the quantity of
    the reactants.

    Args: 
    rnet : The configured reaction network
    initial : 1d array of the initial values for each reactant.
    times : 1d array of time increments to use during simulation.

    Returns:
    reactants : 2d array of the reactant quantities at each time step.
    """
    pass



def simulate_differential_equations(f, x0, t0, tf, dt, noise_intensity=0.0, noise_type='white', num_steps=1000):
    """
    Simulate a system of differential equations with stochasticity.
    
    Parameters:
    - f: function that returns the deterministic system dynamics dx/dt
    - x0: Initial condition for the system
    - t0: Start time
    - tf: End time
    - dt: Time step
    - noise_intensity: Strength of the stochastic noise (default 0.0 = no noise)
    - noise_type: Type of noise ('white' for Gaussian white noise)
    - num_steps: Number of simulation steps
    
    Returns:
    - time: Array of time points
    - x: Array of system states over time
    """
    # Initialize time and state arrays
    time = np.linspace(t0, tf, num_steps)
    x = np.zeros((num_steps, len(x0)))
    x[0] = x0
    
    for i in range(1, num_steps):
        # Compute deterministic part (dx/dt = f(x,t))
        dx = f(x[i-1], time[i-1]) * dt
        
        # Add stochasticity (Gaussian noise if white noise is selected)
        if noise_intensity > 0.0:
            if noise_type == 'white':
                noise = np.random.normal(0, noise_intensity, size=x[i-1].shape)
            else:
                raise ValueError("Unsupported noise type")
            dx += noise
        
        # Update the state with the deterministic and stochastic parts
        x[i] = x[i-1] + dx
    
    return time, x

# Example system: Simple harmonic oscillator (deterministic part)
def harmonic_oscillator(x, t):
    # Simple harmonic oscillator: dx/dt = v, dv/dt = -x (using position and velocity)
    position, velocity = x
    return np.array([velocity, -position])

# Set parameters
x0 = np.array([1.0, 0.0])  # Initial conditions (position = 1, velocity = 0)
t0 = 0.0  # Start time
tf = 20.0  # End time
dt = 0.01  # Time step
noise_intensity = 0.1  # Stochasticity level (0 for no noise)
num_steps = int((tf - t0) / dt)

# Run the simulation
time, x = simulate_differential_equations(harmonic_oscillator, x0, t0, tf, dt, noise_intensity=noise_intensity, num_steps=num_steps)

