# BIO230 Final Project

# Usage Instructions
Run with:
`python main.py [subcommand] [args]`


Basic example:
```bash
python main.py generate --output_file network.pickle
python main.py simulate --input_network_file network.pickle --output_dir network_runs

# Installing dependencies
Requires python>=3.10. May work with previous versions but this isn't tested.

To install dependencies:
`pip install -r requirements.txt`

# Testing
A minimal test suite is included to verify the functionality of the library. To exectute the tests, run `pytest`.
