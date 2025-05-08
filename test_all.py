"""
tests.py

Confirm functionality of the program
"""

from functools import partial

import matplotlib.pyplot as plt
import numpy as np
import pytest
import sympy as sp

from src.diff_eq_generator import (
    ReactionNetwork,
    create_callables,
    generate_reaction_network,
)
from src.diff_eq_simulator import (simulate_differential_equation,
    simulate_network)
from src.utils import lotka_volterra, derivative_finder_diff


class TestGenerator:
    def test_generate_reaction_network(self):
        """
        verify that a roughly correct network is created
        """
        num_species = 3
        rnet = generate_reaction_network(
            num_species=3,
            num_reactions=4,
            seed=42,
        )
        print(rnet.species)
        assert rnet.species == sp.symbols(f'x0:{num_species}')
        print(rnet.odes)
        assert len(rnet.odes) == 3
        print(rnet.reactions)
        assert len(rnet.reactions) == 4

    def test_create_callables(self):
        """
        verify that callable methods are created
        """
        rnet = generate_reaction_network(
            num_species=3,
            num_reactions=4,
            seed=14,
        )
        callables = create_callables(rnet.species, rnet.odes)
        assert len(callables) == 3
        targets = [7.2, 5.1, 5.1]
        for call_func, target in zip(callables, targets):
            result = call_func(1,2,3)
            assert (result - target) < 0.2


class TestSimulator:
    def test_simulate_network(self):
        rnet = generate_reaction_network(
            num_species=3,
            num_reactions=4,
            seed=42,
        )
        reactants, times = simulate_network(
            rnet,
            x0=np.array([1.5, 3.8, 2.5]),
            t0=0,
            tf=1,
            num_steps=20,
        )
        print(reactants)
        print(times)
        # enable this to check output
        if False:
            fig = plt.figure()
            fig.set_size_inches(12, 6)
            axes = fig.subplots(1,2)
            for idx in range(reactants.shape[1]):
                axes[0].plot(times, reactants[:,idx], label=f"{idx}, a")
                # axes[1].plot(reactants[:,0], reactants[:,1], label=f"{idx}")
            axes[0].legend()
            axes[1].legend()
            plt.savefig('test_simulate_differential_equations.png')


    def test_simulate_differential_equation(self):
        species, times = simulate_differential_equation(
            lotka_volterra,
            x0=np.array([1.5,2.5]),
            t0=0,
            tf=10,
            num_steps=200,
        )

        print(species)
        print(times)
        # enable this to check output
        if False:
            fig = plt.figure()
            fig.set_size_inches(12, 6)
            axes = fig.subplots(1,2)
            for idx, track in enumerate([0]):
                axes[0].plot(times, species[:,0], label=f"{idx}, a")
                axes[0].plot(times, species[:,1], label=f"{idx}, b")
                axes[1].plot(species[:,0], species[:,1], label=f"{idx}")
            axes[0].legend()
            axes[1].legend()
            plt.savefig('test_simulate_differential_equations.png')


class TestRecreator:
    pass


class TestUtils:
    def test_derivative_finder_diff(self):
        data = np.array([[1,4.3], [2,7.0]])
        result = derivative_finder_diff(
            data,
            np.array([0.0,2.0]),
        )
        assert np.all(np.abs(result - np.array([[0.5, 2.7/2]])) < 1e-5)


