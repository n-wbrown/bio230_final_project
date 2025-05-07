"""
tests.py

Confirm functionality of the program
"""

import pytest
import sympy as sp

from src.diff_eq_generator import (ReactionNetwork, generate_reaction_network,
    create_callables)
# from src.diff_eq_simulator import ()
# from src.diff_eq_recreator import ()
# src.plot_tools, src.utils


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
            seed=42,
        )
        callables = create_callables(rnet.species, rnet.odes)
        assert len(callables) == 3
        targets = [-1.4, 11.8, -20.2]
        for call_func, target in zip(callables, targets):
            result = call_func(1,2,3)
            assert (result - target) < 0.2


class TestSimulator:
    pass


class TestRecreator:
    pass
