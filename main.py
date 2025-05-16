import argparse

import src.diff_eq_generator, src.diff_eq_simulator, src.diff_eq_recreator, src.plot_tools, src.utils


# constants
SUBPARSER_KEY = "subparser"
GENERATE_NAME = "generate"
SIMULATE_NAME = "simulate"
RECREATE_NAME = "recreate"
PLOT_TOOL_NAME = "plot_tool"  # deprecated



def parse_cl_args():
    parser = argparse.ArgumentParser(
        prog='bio_230_final_project',
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
        default=4,
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
        default=1e-3,
    )
    simulate_subparser.add_argument(
        "--output_file",
        help="Directory to save the saved reactants to",
        default=None,
        type=str,
    )

    # Aim 3: Use the time series data to try and recreate the original differential equation
    recreate_subparser = subparsers.add_parser(
        name=RECREATE_NAME,
        help="Create a set of differential equations from the time-series data",
    )
    recreate_subparser.add_argument(
        "--input_network_dir",
        help="Directory name of the saved simulation",
        type=str,
    )
    recreate_subparser.add_argument(
        "--niterations",
        help="Number of fitting iterations to run. More iterations improves accuracty",
        type=int,
        default=40,
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

    print(parser.parse_args())
    return parser


if __name__ == "__main__":
    parser = parse_cl_args()
    args = parser.parse_args()
    print(type(args))
    use_subparser = args.__getattribute__(SUBPARSER_KEY)
    if use_subparser is None:
        parser.print_help()
    elif use_subparser ==  GENERATE_NAME:
        # print(GENERATE_NAME)
        # Call methods from diff_eq_generator
        src.diff_eq_generator.example_function()
    elif use_subparser ==  SIMULATE_NAME:
        # print(SIMULATE_NAME)
        # Call methods from diff_eq_simulator
        src.diff_eq_simulator.example_function()
    elif use_subparser ==  RECREATE_NAME:
        # print(RECREATE_NAME)
        # Call methods from diff_eq_recreator
        src.diff_eq_recreator.example_function()
    elif use_subparser ==  PLOT_TOOL_NAME:
        # print(PLOT_TOOL_NAME)
        # Call methods from plot_tools
        src.plot_tools.example_function()

