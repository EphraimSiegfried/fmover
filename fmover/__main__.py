import os.path

import fmover.cli as cli
from fmover.configs import MoveConfigsHandler
from fmover.mover import Mover
import appdirs
from fmover.base_logger import logger


def main():
    # Parse arguments
    args = cli.enable_argument_parser().parse_args()
    # Initialize Configuration Handler
    c_handler = MoveConfigsHandler(appdirs.user_config_dir("fmover"))

    # The user wants to list all configurations
    if args.listConfigs:
        c_handler.print_configs()

    # The user wants to open a given configuration file in a editor
    if args.openConfig:
        try:
            c_handler.open_config(args.openConfig)
        except (FileNotFoundError, OSError) as e:
            logger.error(e)
            exit(1)

    # The user wants to print the content of a given configuration file
    if args.printConfig:
        try:
            c_handler.print_config_content(args.printConfig)
        except FileNotFoundError as e:
            logger.error(e)
            exit(1)

    # The user wants to create a new configuration file with a given basename
    if args.createConfig:
        try:
            c_handler.create_config(args.createConfig)
            print("Configuration file created. The new list of configurations is:")
            c_handler.print_configs()
        except FileExistsError as e:
            input(f"Configuration file already exists. Do you want to overwrite it? [y/N] ")
            if input().lower() == "y":
                c_handler.delete_config(args.createConfig)
                c_handler.create_config(args.createConfig)

    # The user wants to delete a configuration file with a given basename
    if args.deleteConfig:
        try:
            answer = input(f"Are you sure to delete {args.deleteConfig}? (y/n)")
            while answer != "y" and answer != "n":
                answer = input("Please enter \"y\" or \"n\" ")
            if answer == "y":
                c_handler.delete_config(args.deleteConfig)
                print("Configuration file deleted. The new list of configurations is:")
                c_handler.print_configs()
        except FileNotFoundError as e:
            logger.error(e)
            exit(1)

    # The user wants to move a single file based on a given configuration and a given file path
    if args.moveOneFile:
        try:
            file_path, config = tuple(args.moveOneFile)
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            Mover(c_handler.get_config_path(config)).move_file(file_path, not args.silent, args.force)
        except (ValueError, FileNotFoundError) as e:
            # The user did not provide a valid configuration file
            logger.error(e)
            exit(1)

    # The user wants to move all files in a directory based on a given configuration and a given directory path
    if args.moveAllFilesInFolder:
        try:
            dir_path, config = tuple(args.moveAllFilesInFolder)
            Mover(c_handler.get_config_path(config)).move_files_in_dir(dir_path, not args.silent, args.force)
        except (ValueError) as e:
            # The user did not provide a valid configuration file
            logger.error(e)
            exit(1)


if __name__ == '__main__':
    main()
