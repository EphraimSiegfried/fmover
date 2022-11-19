import argparse
import os


def enable_argument_parser():
    argument_parser = argparse.ArgumentParser(
        prog="mover",
        description="Move files based on given rules and file properties"
    )

    argument_parser.add_argument(
        "-l", "--list",
        action="store_true",
        dest="listConfigs",
        help="List all configurations"
    )

    configs = os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "configurations"))
    configs = [c.replace('.json', '') for c in configs]
    argument_parser.add_argument(
        "-o", "--open",
        choices=configs,
        type=str,
        dest="openConfig",
        help="Open configuration file")

    argument_parser.add_argument(
        "-p", "--print",
        choices=configs,
        type=str,
        dest="printConfig",
        help="Print configuration")

    argument_parser.add_argument(
        "-n", "--new",
        type=str,
        metavar="configName",
        dest="createConfig",
        help="Create configuration with given name")

    argument_parser.add_argument(
        "-d", "--delete",
        type=str,
        choices=configs,
        metavar="configName",
        dest="deleteConfig",
        help="Delete a configuration"
    )

    argument_parser.add_argument(
        "-m", "--move",
        nargs=2,
        dest="moveOneFile",
        metavar="pathToFile",
        type=str,
        help="Move given file based on given configuration")

    argument_parser.add_argument(
        "-a", "--all",
        metavar="pathToFolderAndConfig",
        nargs=2,
        dest="moveAllFilesInFolder",
        type=str,
        help="Move all files in the current folder based on given configuration")

    return argument_parser


def existing_file_path(file_path):
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"The file: \"{file_path}\" does not exist")
    elif os.path.isdir(file_path):
        raise argparse.ArgumentTypeError(f"The file \"{file_path}\" is a directory and not a file")
    return file_path
