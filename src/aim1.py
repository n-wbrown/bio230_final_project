# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 10:43:50 2025

@author: kathe
"""

#hello edit
import sympy as sp
import numpy as np

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
        species (list): List of sympy symbols for species.
        odes (list): List of sympy expressions representing d[species]/dt.
        reactions (list): List of reaction dictionaries.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Define species symbols
    species = sp.symbols(f'x0:{num_species}')
    odes = [0 for _ in range(num_species)]
    reactions = []
    
    for _ in range(num_reactions):
        # Randomly choose number of reactants and products
        n_reactants = np.random.randint(1, max_reactants + 1)
        n_products = np.random.randint(1, max_products + 1)
        
        # Randomly choose which species are reactants and products
        reactant_idxs = np.random.choice(range(num_species), n_reactants, replace=False)
        product_idxs = np.random.choice(range(num_species), n_products, replace=False)
        
        # Randomly assign stoichiometric coefficients (1 or 2)
        reactant_stoich = np.random.randint(1, 3, n_reactants)
        product_stoich = np.random.randint(1, 3, n_products)
        
        # Random rate constant
        rate = np.round(np.random.uniform(*rate_range), 3)
        
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
    
    return species, odes, reactions

# Example usage:
species, odes, reactions = generate_reaction_network(num_species=3, num_reactions=4, seed=42)

print("Species:", species)
print("\nODEs:")
for i, ode in enumerate(odes):
    print(f"d{species[i]}/dt = {sp.simplify(ode)}")

print("\nReactions:")
for rxn in reactions:
    print(rxn)

