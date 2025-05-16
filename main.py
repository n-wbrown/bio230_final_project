import argparse
import pickle
from sys import maxsize
import numpy as np
import os
from pathlib import Path
import logging
import glob

import src.diff_eq_generator, src.diff_eq_simulator, src.diff_eq_recreator, src.plot_tools, src.utils


# constants
SUBPARSER_KEY = "subparser"
GENERATE_NAME = "generate"
SIMULATE_NAME = "simulate"
RECREATE_NAME = "recreate"

REACTANTS_SUFFIX = "_reactants"
TIMES_SUFFIX = "_times"

# logger
logger = logging.getLogger(__name__)


def generate_runner(args: argparse.Namespace) -> None:
    rnet = src.diff_eq_generator.generate_reaction_network(
        num_species=args.num_species,
        num_reactions=args.num_reactions,
        max_reactants=args.max_reactants,
        max_products=args.max_products,
        seed=args.seed,
    )
    for eq in rnet.odes:
        print(f"generated: {eq}")

    if args.output_file is not None:
        with open(args.output_file, "wb") as out_file:
            pickle.dump(rnet, out_file)
            logger.info(f"saved {args.output_file}")


def simulate_runner(args: argparse.Namespace) -> None:
    if os.path.isdir(args.output_dir):
        logger.warning("output directory with that name already exists")
        exit()

    rnet = None
    with open(args.input_network_file, "rb") as in_file:
        rnet = pickle.load(in_file)

    reactants_results, times_results = src.diff_eq_recreator.rand_runner(
        rnet=rnet,
        ubound=np.array([args.ubound] * len(rnet.species)),
        steps=args.steps,
        noise_intensity=np.array([args.noise_intensity] * len(rnet.species)),
        run_duration=args.run_duration,
        runs=args.runs,
    )

    os.mkdir(args.output_dir)
    for idx, (reactants, times) in enumerate(zip(reactants_results, times_results)):
        reactants_path = Path(Path(args.output_dir), Path(f"{idx}{REACTANTS_SUFFIX}"))
        np.save(
            reactants_path,
            reactants,
        )
        logger.info(f"saved {reactants_path}")
        times_path = Path(Path(args.output_dir), Path(f"{idx}{TIMES_SUFFIX}"))
        np.save(
            times_path,
            times,
        )
        logger.info(f"saved {times_path}")


def recreate_runner(args: argparse.Namespace) -> None:
    if not os.path.isdir(args.input_sim_dir):
        logger.warning("output directory with that name already exists")
        exit()

    reactants_filenames = glob.glob(
        f"*{REACTANTS_SUFFIX}*",
        dir_fd=args.input_sim_dir,
    )
    reactants_filenames.sort()

    times_filenames = glob.glob(
        f"*{TIMES_SUFFIX}*",
        dir_fd=args.input_sim_dir,
    )
    times_filenames.sort()

    logger.debug(f"{reactants_filenames}")
    logger.debug(f"{times_filenames}")

    reactants_arrays = []
    times_arrays = []

    for reactants_filename, times_filename in zip(reactants_filenames, times_filenames):
        reactants_path = Path(Path(args.input_sim_dir), Path(reactants_filename))
        logger.debug(f"loading: {reactants_path}")
        reactants_arrays.append(np.load(reactants_path))
        times_path = Path(Path(args.input_sim_dir), Path(times_filename))
        logger.debug(f"loading: {times_path}")
        times_arrays.append(np.load(times_path))

    merged_qty_data, _, merged_qty_drv = src.diff_eq_recreator.data_set_bundler(
        reactants_arrays,
        times_arrays,
    )
    model = src.diff_eq_recreator.regressor_fit(
        merged_qty_data,
        merged_qty_drv,
        maxsize=args.maxsize,
        niterations=args.niterations,
    )

    output_buf = []
    for eq in model.equations_:
        output_buf.append(eq[["complexity", "loss", "score", "equation", "sympy_format"]].to_string())
        output_buf.append("\n")

    for best in model.get_best():
        output_buf.append(best.to_string())
        output_buf.append("\n")

    output_msg = "\n".join(output_buf)

    if args.output is not None:
        with open(args.output, "w") as out_file:
            out_file.write(output_msg)

    else:
        print(output_msg)


def parse_cl_args():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Solve stochastic differential equations and approximate the original equation.",
    )
    subparsers = parser.add_subparsers(
        dest=SUBPARSER_KEY,
    )

    # Aim 1: Generate equations
    generate_subparser = subparsers.add_parser(
        name=GENERATE_NAME,
        help="Generate differential equations for simulation.",
    )
    generate_subparser.add_argument(
        "--num_species",
        help="Number of unique species to include in the network",
        default=3,
        type=int,
    )
    generate_subparser.add_argument(
        "--num_reactions",
        help="Number of reaction paths to include in the network",
        default=3,
        type=int,
    )
    generate_subparser.add_argument(
        "--max_reactants",
        help="Number of reactants allowed per reaction path",
        default=2,
        type=int,
    )
    generate_subparser.add_argument(
        "--max_products",
        help="Number of products allowed per reaction path",
        default=2,
        type=int,
    )
    generate_subparser.add_argument(
        "--seed",
        help="Set the random number seed for repeatable network generation",
        default=None,
        type=int,
    )
    generate_subparser.add_argument(
        "--output_file",
        help="Filename to save the network to",
        default=None,
        type=str,
    )

    # Aim 2: Simulate the equation with stochasticity
    simulate_subparser = subparsers.add_parser(
        name=SIMULATE_NAME,
        help="take a differential equation as input and simulate the system with stochasticity",
    )
    simulate_subparser.add_argument(
        "--input_network_file",
        help="Filename of the saved reaction network to simulate",
        type=str,
        required=True,
    )
    simulate_subparser.add_argument(
        "--ubound",
        help="Upper bound for randomized initial conditions.",
        type=float,
        default=1.0,
    )
    simulate_subparser.add_argument(
        "--steps",
        help="number of simulation steps to execute",
        type=int,
        default=50,
    )
    simulate_subparser.add_argument(
        "--run_duration",
        help="Simulation time to run for",
        type=float,
        default=1,
    )
    simulate_subparser.add_argument(
        "--noise_intensity",
        help="Per-step noise to add to the simulation",
        type=float,
        default=1e-4,
    )
    simulate_subparser.add_argument(
        "--runs",
        help="number of independent simulations to create",
        type=int,
        default=20,
    )
    simulate_subparser.add_argument(
        "--output_dir",
        help="Directory to save the saved reactants to",
        type=str,
        required=True,
    )

    # Aim 3: Use the time series data to try and recreate the original differential equation
    recreate_subparser = subparsers.add_parser(
        name=RECREATE_NAME,
        help="Create a set of differential equations from the time-series data",
    )
    recreate_subparser.add_argument(
        "--input_sim_dir",
        help="Directory name of the saved simulation",
        type=str,
        required=True,
    )
    recreate_subparser.add_argument(
        "--niterations",
        help="Number of fitting iterations to run. More iterations improves accuracty",
        type=int,
        default=100,
    )
    recreate_subparser.add_argument(
        "--maxsize",
        help="Restrict the maximum complexity of the explored solutions",
        type=int,
        default=20,
    )
    recreate_subparser.add_argument(
        "--output",
        help="Print the results into the file",
        type=str,
        default=None,
    )

    logger.debug(f"{parser.parse_args()=}")
    return parser


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    parser = parse_cl_args()
    args = parser.parse_args()
    use_subparser = args.__getattribute__(SUBPARSER_KEY)
    if use_subparser is None:
        parser.print_help()
    elif use_subparser == GENERATE_NAME:
        # print(GENERATE_NAME)
        # Call methods from diff_eq_generator
        generate_runner(args)
    elif use_subparser == SIMULATE_NAME:
        # print(SIMULATE_NAME)
        # Call methods from diff_eq_simulator
        simulate_runner(args)
    elif use_subparser == RECREATE_NAME:
        # print(RECREATE_NAME)
        # Call methods from diff_eq_recreator
        recreate_runner(args)
