# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 10:43:50 2025

@author: kathe
"""

from dataclasses import dataclass, field

import sympy as sp
import numpy as np



def example_function():
    print(f"the example function in {__file__} is running")


@dataclass
class ReactionNetwork:
    """
    species (list): List of sympy symbols for species.
    odes (list): List of sympy expressions representing d[species]/dt.
    reactions (list): List of reaction dictionaries.
    """
    species: list[sp.core.symbol.Symbol]
    odes: list
    reactions: list[dict]


def generate_reaction_network(num_species=3, num_reactions=4, 
                              max_reactants=2, max_products=2, 
                              rate_range=(0.1, 2.0), seed=None):
    """
    Generate a random reaction network as a set of symbolic ODEs.

    Args:
        num_species (int): Number of chemical species.
        num_reactions (int): Number of reactions.
        max_reactants (int): Maximum number of reactants per reaction.
        max_products (int): Maximum number of products per reaction.
        rate_range (tuple): Range for random rate constants.
        seed (int or None): Random seed for reproducibility.

    Returns:
        network (ReactionNetwork): object containing the species list, odes, and reactions
    """
    rng = np.random.default_rng(seed=seed)
    
    # Define species symbols
    species = sp.symbols(f'x0:{num_species}')
    odes = [0 for _ in range(num_species)]
    reactions = []
    
    for _ in range(num_reactions):
        # Randomly choose number of reactants and products
        n_reactants = rng.integers(1, max_reactants + 1)
        n_products = rng.integers(1, max_products + 1)
        
        # Randomly choose which species are reactants and products
        reactant_idxs = rng.choice(range(num_species), n_reactants, replace=False)
        product_idxs = rng.choice(range(num_species), n_products, replace=False)
        
        # Randomly assign stoichiometric coefficients (1 or 2)
        reactant_stoich = rng.integers(1, 3, n_reactants)
        product_stoich = rng.integers(1, 3, n_products)
        
        # Random rate constant
        rate = np.round(rng.uniform(*rate_range), 3)
        
        # Build rate law: product of reactant concentrations to their stoichiometric powers
        rate_law = rate
        for idx, stoich in zip(reactant_idxs, reactant_stoich):
            rate_law *= species[idx] ** stoich
        
        # Update ODEs: subtract for reactants, add for products
        for idx, stoich in zip(reactant_idxs, reactant_stoich):
            odes[idx] -= stoich * rate_law
        for idx, stoich in zip(product_idxs, product_stoich):
            odes[idx] += stoich * rate_law
        
        # Store reaction info for reference
        reactions.append({
            'reactants': {str(species[idx]): int(stoich) for idx, stoich in zip(reactant_idxs, reactant_stoich)},
            'products': {str(species[idx]): int(stoich) for idx, stoich in zip(product_idxs, product_stoich)},
            'rate_constant': float(rate)
        })
    
    return ReactionNetwork(
        species=species,
        odes=odes,
        reactions=reactions,
    )


def create_callables(species: list[sp.core.symbol.Symbol], odes: list) -> list:
    """
    Generate a set of callables corresponding to the differentaial equations of a ReactionNetwork.

    Args:
        species: List of sympy symbols representing each species' quantity
        odes: list of ordinary differential equation represented by sympy functions

    Returns:
        network: list of callable functions corresponding to the given odes list
    """
    x_eqs = []
    species_count = len(species)

    for ode in odes:
        specs = sp.symbols(f"i0:{species_count}")
        lam = sp.lambdify(specs, ode.evalf(subs={species[k]: specs[k] for k in range(species_count)}))
        x_eqs.append(lam)

    return x_eqs


if __name__ == "__main__":
    # Example usage:
    rnet = generate_reaction_network(num_species=3, num_reactions=4, seed=42)
    species = rnet.species
    odes = rnet.odes
    reactions = rnet.reactions

    print("Species:", species)
    print("\nODEs:")
    for i, ode in enumerate(odes):
        print(f"d{species[i]}/dt = {sp.simplify(ode)}")

    print("\nReactions:")
    for rxn in reactions:
        print(rxn)

