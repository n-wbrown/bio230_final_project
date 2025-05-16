# BIO230 Final Project

Final project submission for UC Merced's Computation and Modeling for Interdisciplinary Biophysical Sciences, Biomaterials and Biotechnology (PHYS 230, Spring 2025)

This project attempts to reconstruct chemical reaction networks from
time-series recording of the reactant quantities. The project includes tools to
generate and simulate networks for testing.


# Getting Started
## Installing dependencies
This tool does not need to be installed but it does require some dependencies
to be installed in your environment before it can be run. This requires
python>=3.10. It may work with previous versions but this isn't tested.

To install dependencies:
```bash
# Using pip:
pip install -r requirements.txt

# Using Conda:
conda install --file requirements.txt
```

## Running the tool
Run with:
`python main.py [subcommand] [args]`

For an extended exmples, see [Example usage](#example-usage)

## Testing
A minimal test suite is included to verify the functionality of the library. To exectute the tests, run `pytest`.

# Example usage
```bash
# Generate the reaction network
python main.py generate --output_file network.pickle

# Simulate the reaction network
python main.py simulate --input_network_file network.pickle --output_dir network_runs

# Process the simulated data and attempt to reconstruct the original network
python main.py recreate --input_sim_dir network_runs
```

## Extended Documentation
### Command Structure
```
usage: python main.py [-h] {generate,simulate,recreate} ...

Solve stochastic differential equations and approximate the original equation.

positional arguments:
  {generate,simulate,recreate}
    generate            Generate differential equations for simulation.
    simulate            take a differential equation as input and simulate the system with stochasticity
    recreate            Create a set of differential equations from the time-series data

options:
  -h, --help            show this help message and exit
```
### Generate
```
usage: python main.py generate [-h] [--num_species NUM_SPECIES] [--num_reactions NUM_REACTIONS] [--max_reactants MAX_REACTANTS] [--max_products MAX_PRODUCTS] [--seed SEED]
                               [--output_file OUTPUT_FILE]

options:
  -h, --help            show this help message and exit
  --num_species NUM_SPECIES
                        Number of unique species to include in the network
  --num_reactions NUM_REACTIONS
                        Number of reaction paths to include in the network
  --max_reactants MAX_REACTANTS
                        Number of reactants allowed per reaction path
  --max_products MAX_PRODUCTS
                        Number of products allowed per reaction path
  --seed SEED           Set the random number seed for repeatable network generation
  --output_file OUTPUT_FILE
                        Filename to save the network to
```
### Simulate
```
usage: python main.py simulate [-h] --input_network_file INPUT_NETWORK_FILE [--ubound UBOUND] [--steps STEPS] [--run_duration RUN_DURATION]
                               [--noise_intensity NOISE_INTENSITY] [--runs RUNS] --output_dir OUTPUT_DIR

options:
  -h, --help            show this help message and exit
  --input_network_file INPUT_NETWORK_FILE
                        Filename of the saved reaction network to simulate
  --ubound UBOUND       Upper bound for randomized initial conditions.
  --steps STEPS         number of simulation steps to execute
  --run_duration RUN_DURATION
                        Simulation time to run for
  --noise_intensity NOISE_INTENSITY
                        Per-step noise to add to the simulation
  --runs RUNS           number of independent simulations to create
  --output_dir OUTPUT_DIR
                        Directory to save the saved reactants to
```
### Recreate
```
usage: python main.py recreate [-h] --input_sim_dir INPUT_SIM_DIR [--niterations NITERATIONS] [--maxsize MAXSIZE] [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --input_sim_dir INPUT_SIM_DIR
                        Directory name of the saved simulation
  --niterations NITERATIONS
                        Number of fitting iterations to run. More iterations improves accuracty
  --maxsize MAXSIZE     Restrict the maximum complexity of the explored solutions
  --output OUTPUT       Print the results into the file
```

# Slides
The presentatio slides can be found [here](slides/PHYS230%20Final%20Project.pdf)

# Ackwnowledgements

This project has been made possible by
- Miles Cranmer's [PySR](https://github.com/MilesCranmer/PySR) package for symbolic regression
- [Perplexity](https://www.perplexity.ai/) for coding assistance
