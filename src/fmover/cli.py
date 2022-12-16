import argparse
from fmover.configs import MoveConfigsHandler
from fmover.mover import Mover
import os
import appdirs

configs_handler = MoveConfigsHandler(appdirs.user_config_dir("fmover"))


def is_file(path: str) -> str:
    """
    Used for argparse to instantly check if the given path is a file.
    Usage is found in the "type" argument of add_argument.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} does not exist")
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"{path} is not a file")
    return path


def is_dir(path: str):
    """
    Used for argparse to instantly check if the given path is a directory.
    Usage is found in the "type" argument of add_argument.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} does not exist")
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a directory")
    return path


def move_file(file_path: str, config_name: str, notify: bool, force: bool) -> None:
    """
    Used to call the move_file method of the Mover class in the "set_defaults" argument of the move_file_parser.
    """
    mover = Mover(configs_handler.get_config_path(config_name))
    mover.move_file(file_path, notify, force)


def move_files_in_dir(dir_path: str, config_name: str, notify: bool, force: bool) -> None:
    """
    Used to call the move_files_in_dir method of the Mover class in the "set_defaults" argument of the move_dir_parser.
    """
    mover = Mover(configs_handler.get_config_path(config_name))
    mover.move_files_in_dir(dir_path, notify, force)


def main():
    """
    This is the entry point for the fmover command line interface.
    In this method, the command line arguments are parsed.
    """
    configs = configs_handler.list_configs()

    # Creates the parser
    arg_parser = argparse.ArgumentParser(
        prog="fmover",
        description="Move files based on given rules and file properties"
    )
    subparsers = arg_parser.add_subparsers(dest="command")

    # List all configuration names
    list_parser = subparsers.add_parser("list", help="List all configurations")
    list_parser.set_defaults(func=configs_handler.print_configs)

    # Create a configuration
    create_config_parser = subparsers.add_parser('create', help='Create a configuration file')
    create_config_parser.add_argument('config_name', help='The name of the configuration file', type=str)
    create_config_parser.set_defaults(func=configs_handler.create_config)

    # Open a configuration
    open_config_parser = subparsers.add_parser('open', help='Open a configuration file')
    open_config_parser.add_argument('config_name', help='The name of the configuration file', choices=configs)
    open_config_parser.set_defaults(func=configs_handler.open_config)

    # Delete a configuration
    delete_config_parser = subparsers.add_parser('delete', help='Delete a configuration file')
    delete_config_parser.add_argument('config_name', help='The name of the configuration file', choices=configs)
    delete_config_parser.set_defaults(func=configs_handler.delete_config)

    # Print a configuration
    print_config_parser = subparsers.add_parser('print', help='Print a configuration file')
    print_config_parser.add_argument('config_name', help='The name of the configuration file', choices=configs)
    print_config_parser.set_defaults(func=configs_handler.print_config_content)

    # Move one file
    move_file_parser = subparsers.add_parser('move', help='Move one file')
    move_file_parser.add_argument('file_path', help='The path of the file', type=is_file)
    move_file_parser.add_argument('config_name',metavar="config_name", help='The name of the configuration file', choices=configs)
    move_file_parser.add_argument('-n', '--notify', action='store_true',
                                  help='Show a notification when the file is moved')
    move_file_parser.add_argument('-f', '--force', action='store_true',
                                  help='Create the destination directory if it does not exist')
    move_file_parser.set_defaults(func=move_file)

    # Move all files in a directory
    move_dir_parser = subparsers.add_parser('move-all', help='Move all files in a directory')
    move_dir_parser.add_argument('dir_path', help='The path of the directory', type=is_dir)
    move_dir_parser.add_argument('config_name', metavar="config_name",help='The name of the configuration file', choices=configs)
    move_dir_parser.add_argument('-n', '--notify', action='store_true',
                                 help='Show a notification when the file is moved')
    move_dir_parser.add_argument('-f', '--force', action='store_true',
                                 help='Create the destination directory if it does not exist')
    move_dir_parser.set_defaults(func=move_files_in_dir)

    # Parse the arguments
    args = arg_parser.parse_args()
    if args.command is None:
        arg_parser.print_help()
        return

    # Call the function
    args = arg_parser.parse_args()
    args_ = vars(args).copy()
    args_.pop('command', None)
    args_.pop('func', None)
    args.func(**args_)


if __name__ == '__main__':
    main()
