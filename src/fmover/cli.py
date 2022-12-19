import argparse
from fmover.configs import MoveConfigsHandler
from fmover.mover import Mover
import os
import appdirs
from typing import Optional, Sequence


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


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    This is the entry point for the fmover command line interface.
    In this method, the command line arguments are parsed.
    """

    # Creates the parser
    arg_parser = argparse.ArgumentParser(
        prog="fmover", description="Move files based on given rules and file properties"
    )
    arg_parser.add_argument(
        "--configdir",
        "-c",
        type=is_dir,
        help="The directory where the configuration files are stored",
    )

    subparsers = arg_parser.add_subparsers(dest="command")

    # List all configuration names
    list_parser = subparsers.add_parser("list", help="List all configurations")
    list_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the full path to the configuration files",
    )

    # Create a configuration
    create_config_parser = subparsers.add_parser(
        "create", help="Create a configuration file"
    )
    create_config_parser.add_argument(
        "config_new_name", help="The name of the configuration file", type=str
    )

    # Open a configuration
    open_config_parser = subparsers.add_parser("open", help="Open a configuration file")
    open_config_parser.add_argument(
        "config_name", help="The name of the configuration file"
    )

    # Delete a configuration
    delete_config_parser = subparsers.add_parser(
        "delete", help="Delete a configuration file"
    )
    delete_config_parser.add_argument(
        "config_name", help="The name of the configuration file"
    )

    # Print a configuration
    print_config_parser = subparsers.add_parser(
        "print", help="Print a configuration file"
    )
    print_config_parser.add_argument(
        "config_name", help="The name of the configuration file"
    )

    # Move one file
    move_file_parser = subparsers.add_parser("move", help="Move one file")
    move_file_parser.add_argument(
        "file_path", help="The path of the file", type=is_file
    )
    move_file_parser.add_argument(
        "config_name", metavar="config_name", help="The name of the configuration file"
    )
    move_file_parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Do not actually move the file, just print the destination",
    )
    move_file_parser.add_argument(
        "-n",
        "--notify",
        action="store_true",
        help="Show a notification when the file is moved",
    )
    move_file_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Create the destination directory if it does not exist",
    )

    # Move all files in a directory
    move_dir_parser = subparsers.add_parser(
        "move-all", help="Move all files in a directory"
    )
    move_dir_parser.add_argument(
        "dir_path", help="The path of the directory", type=is_dir
    )
    move_dir_parser.add_argument(
        "config_name", metavar="config_name", help="The name of the configuration file"
    )
    move_dir_parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Do not actually move the file, just print the destination",
    )
    move_dir_parser.add_argument(
        "-n",
        "--notify",
        action="store_true",
        help="Show a notification when the file is moved",
    )
    move_dir_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Create the destination directory if it does not exist",
    )

    # Parse the arguments
    args = arg_parser.parse_args(argv)
    if args.configdir:
        config_dir = args.configdir
    elif os.path.exists(os.path.dirname(appdirs.user_config_dir("fmover"))):
        config_dir = appdirs.user_config_dir("fmover")
    else:
        config_dir = os.path.dirname(os.path.abspath(__file__))
    configs_handler = MoveConfigsHandler(config_dir)

    if not args.command:
        arg_parser.print_help()
        return
    if (
        hasattr(args, "config_name")
        and args.config_name not in configs_handler.list_configs()
    ):
        print(
            f"The configuration '{args.config_name}' does not exist. "
            f"Choose one of the following configurations: {configs_handler.list_configs()} or create a new one."
        )
        return
    if args.command == "list":
        configs_handler.print_configs(verbose=args.verbose)
    elif args.command == "create":
        configs_handler.create_config(args.config_new_name)
    elif args.command == "open":
        configs_handler.open_config(args.config_name)
    elif args.command == "delete":
        configs_handler.delete_config(args.config_name)
    elif args.command == "print":
        configs_handler.print_config_content(args.config_name)
    elif args.command == "move":
        mover = Mover(configs_handler.get_config_path(args.config_name))
        mover.move_file(
            args.file_path,
            should_notify=args.notify,
            force=args.force,
            dry_run=args.dry_run,
        )
    elif args.command == "move-all":
        mover = Mover(configs_handler.get_config_path(args.config_name))
        mover.move_files_in_dir(
            args.dir_path,
            should_notify=args.notify,
            force=args.force,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    exit(main())
