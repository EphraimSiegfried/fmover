import fmover.cli as cli
import fmover.configs as configs
from fmover.mover import Mover
import logging


def main():
    # Parse arguments
    args = cli.enable_argument_parser().parse_args()

    # The user wants to list all configurations
    if args.listConfigs:
        configs.print_list_configurations()

    # The user wants to open a given configuration file in a editor
    if args.openConfig:
        configs.open_configuration(args.openConfig)

    # The user wants to print the content of a given configuration file
    if args.printConfig:
        configs.print_configuration(args.printConfig)

    # The user wants to create a new configuration file with a given basename
    if args.createConfig:
        configs.create_configuration(args.createConfig)

    # The user wants to delete a configuration file with a given basename
    if args.deleteConfig:
        answer = input(f"Are you sure to delete {args.deleteConfig}? (y/n)")
        while answer != "y" and answer != "n":
            answer = input("Please enter \"y\" or \"n\" ")
        if answer == "y":
            configs.delete_configuration(args.deleteConfig)

    # The user wants to move a single file based on a given configuration and a given file path
    if args.moveOneFile:
        file_path, config = tuple(args.moveOneFile)
        Mover(configs.get_config_path(config)).move_file(file_path, not args.silent)

    # The user wants to move all files in a directory based on a given configuration and a given directory path
    if args.moveAllFilesInFolder:
        dir_path, config = tuple(args.moveAllFilesInFolder)
        Mover(configs.get_config_path(config)).move_files_in_dir(dir_path, not args.silent)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("fmover.log")
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    # Create formatters and add it to handlers
    file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_format = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_format)
    console_handler.setFormatter(console_format)
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    main()
