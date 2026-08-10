"""
Description:
This script runs the validation simulation scenarios defined in the
validation scenarios folder.

Usage:
Run the script from the command line with the following syntax:
  python scripts/run_validation.py

Dependencies:
See requirements.txt (install using `pip install -r requirements.txt`).
"""

import glob
import os
import argparse
import shutil
import subprocess
import logging

from sbmlpbkutils import load_config, run_config, plot_simulation_results

CONFIGS_PATH = './validation/scenarios/'
OUTPUT_PATH = './validation/results'
R_CONFIGS = [
    {
        'id': 'R_repeated_dose',
        'file_path': 'validation/R/run_westerhout_2024.R',
        'output_files': [
            './validation/results/results_R_PFAS.csv'
        ]
    },
    {
        'id': 'R_no_dosing',
        'file_path': 'validation/R/run_westerhout_2024_no_dosing.R',
        'output_files': [
            './validation/results/results_R_PFAS_no_dosing.csv'
        ]
    }
]

def run_validation(configs: list[str], force_recompute: bool, skip_r: bool):

    # Configure logger for formatted console output
    logger = logging.getLogger('run_validation')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    if not logger.handlers:
        logger.addHandler(console_handler)

    # Run R validaton scenarios
    if not skip_r:
        run_r_validation_scenarios(force_recompute, logger)

    # Glob scenario configs and run them
    for file in configs:
        file_dir = os.path.dirname(file)

        # Load config
        config = load_config(file)

        # Create output directory if it does not exist
        out_path = os.path.join(OUTPUT_PATH, os.path.relpath(file_dir, CONFIGS_PATH), config.id)

        # Ensure config output path
        os.makedirs(out_path, exist_ok=True)

        # Run simulations
        logger.info("Running simulation config %s", file)
        run_config(
            config = config,
            out_path = out_path,
            force_recompute = force_recompute,
            logger = logger
        )

        # Run simulations
        plot_simulation_results(
            config = config,
            out_path = out_path
        )

def run_r_validation_scenarios(
    force_recompute: bool,
    logger: logging.Logger
):
    for r_config in R_CONFIGS:
        out_files = r_config['output_files']
        if not force_recompute and all([os.path.exists(o) for o in out_files]):
            logger.info(f"Skipping {r_config['id']} validation scenarios: results already available")
            return

        # Run R validation scenarios
        logger.info("Running R validation scenarios")
        subprocess.run(['Rscript', r_config['file_path']], check=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run validation scripts arguments.")
    parser.add_argument(
        '--configs',
        '-c',
        nargs='+',
        default=None,
        help='Specific YAML config file(s) to run. If not specified, all configs in CONFIGS_PATH are used.'
    )
    parser.add_argument(
        '-f',
        '--force_recompute',
        action="store_true",
        default=False,
        help="Force re-calculation of validation results instead of using cached results."
    )
    parser.add_argument(
        '--skip_r',
        action="store_true",
        default=False,
        help="Force re-calculation of validation results instead of using cached results."
    )
    args = parser.parse_args()

    if args.configs:
        configs = args.configs
    else:
        configs = glob.glob(f'./{CONFIGS_PATH}/**/*.yaml', recursive=True)
    force_recompute = args.force_recompute
    skip_r = args.skip_r

    run_validation(configs, force_recompute, skip_r)
