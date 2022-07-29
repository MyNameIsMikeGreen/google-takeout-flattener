import argparse
import glob
import logging
import os
import zipfile
from pathlib import Path

from tqdm import tqdm


def main(input_directory: Path, output_directory: Path):
    create_dir_if_not_exists(output_directory)
    takeout_file_paths = glob.glob(f"{input_directory}/takeout-*.zip")
    logging.info(f"Found {len(takeout_file_paths)} Google Takeout files")
    for takeout_file_path in tqdm(iterable=takeout_file_paths, unit="ZIP File"):
        logging.debug(f"Extracting {takeout_file_path}...")
        with zipfile.ZipFile(takeout_file_path, 'r') as takeout_file:
            for file in takeout_file.namelist():
                try:
                    takeout_file.extract(member=file, path=output_directory)
                except OSError as error:
                    logging.warning(f"Skipped file {file} due to OSError: {str(error)}")
        logging.debug(f"{takeout_file_path} successfully extracted")
    logging.info("Successfully unzipped all files")


def create_dir_if_not_exists(dir):
    if not dir.is_dir():
        logging.debug(f"{dir} does not exist. Creating...")
        os.makedirs(dir, exist_ok=True)
        logging.debug(f"{dir} created")


def _set_up_logging(log_level_string):
    log_level = getattr(logging, log_level_string.upper(), None)
    logging.basicConfig(level=log_level, filename="google-takeout-flattener.log", filemode='w')


def _parse_arguments():
    parser = argparse.ArgumentParser()
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    log_levels.extend([level.lower() for level in log_levels])
    parser.add_argument("input_directory", help="Directory containing all Google Takeout files to flatten", type=Path)
    parser.add_argument("output_directory", help="Directory to have the flattened input files output to", type=Path)
    parser.add_argument("--log_level", choices=log_levels, default="INFO")
    return parser.parse_args()


def _validate_arguments(args):
    if not args.input_directory.is_dir():
        logging.error(f"Input directory ({args.input_directory}) does not exist")
        exit(-1)
    if str(args.output_directory).startswith(str(args.input_directory)):
        logging.error(f"Output directory ({args.output_directory}) must not reside within input directory ({args.input_directory})")
        exit(-2)
    if args.output_directory.is_file():
        logging.error(f"Supplied output directory ({args.output_directory}) is an existing file")
        exit(-3)


if __name__ == '__main__':
    args = _parse_arguments()
    _set_up_logging(args.log_level)
    _validate_arguments(args)
    main(args.input_directory, args.output_directory)
