import argparse

import src.diff_eq_generator, src.diff_eq_simulator, src.diff_eq_recreator, src.plot_tools, src.utils


# constants
SUBPARSER_KEY = "subparser"
GENERATE_NAME = "generate"
SIMULATE_NAME = "simulate"
RECREATE_NAME = "recreate"
PLOT_TOOL_NAME = "plot_tool"


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
        "example",
        help="this is an example of how to pass an argument to a subparser",
    )

    # Aim 2: Simulate the equation with stochasticity
    simulate_subparser = subparsers.add_parser(
        name=SIMULATE_NAME,
        help="take a differential equation as input and simulate the system with stochasticity",
    )

    # Aim 3: Use the time series data to try and recreate the original differential equation
    recreate_subparser = subparsers.add_parser(
        name=RECREATE_NAME,
        help="Create a set of differential equations from the time-series data",
    )

    # plotter
    recreate_subparser = subparsers.add_parser(
        name=PLOT_TOOL_NAME,
        help="tools plotting simulated data",
    )

    print(parser.parse_args())
    return parser


if __name__ == "__main__":
    parser = parse_cl_args()
    args = parser.parse_args()
    use_subparser = args.__getattribute__(SUBPARSER_KEY)
    if use_subparser is None:
        parser.print_help()
    elif use_subparser ==  GENERATE_NAME:
        print(GENERATE_NAME)
        # Call methods from diff_eq_generator
        src.diff_eq_generator.example_function()
    elif use_subparser ==  SIMULATE_NAME:
        print(SIMULATE_NAME)
        # Call methods from diff_eq_simulator
        src.diff_eq_simulator.example_function()
    elif use_subparser ==  RECREATE_NAME:
        print(RECREATE_NAME)
        # Call methods from diff_eq_recreator
        src.diff_eq_recreator.example_function()
    elif use_subparser ==  PLOT_TOOL_NAME:
        print(PLOT_TOOL_NAME)
        # Call methods from plot_tools
        src.plot_tools.example_function()
        

