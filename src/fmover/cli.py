import argparse


def enable_argument_parser() -> argparse.ArgumentParser:
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

    argument_parser.add_argument(
        "-o", "--open",
        type=str,
        dest="openConfig",
        help="Open configuration file")

    argument_parser.add_argument(
        "-p", "--print",
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
        metavar="configName",
        dest="deleteConfig",
        help="Delete a configuration"
    )

    argument_parser.add_argument(
        "-m", "--move",
        nargs=2,
        dest="moveOneFile",
        metavar=("pathToFile", "configName"),
        type=str,
        help="Move given file based on given configuration")

    argument_parser.add_argument(
        "-a", "--all",
        metavar=("pathToFolder", "configName"),
        nargs=2,
        dest="moveAllFilesInFolder",
        type=str,
        help="Move all files in the given folder based on given configuration")

    argument_parser.add_argument(
        "-s", "--silent",
        action="store_true",
        dest="silent",
        help="Do not notify that the file has been moved")

    # Optional force argument which creates a destination directory if it does not exist
    argument_parser.add_argument(
        "-f", "--force",
        action="store_true",
        dest="force",
        help="Create destination directory if it does not exist")

    return argument_parser
