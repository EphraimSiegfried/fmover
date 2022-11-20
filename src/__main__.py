import src.cli as cli
import src.configs as configs
from src.mover import Mover


def main():
    args = cli.enable_argument_parser().parse_args()
    if args.listConfigs:
        configs.print_list_configurations()
    elif args.openConfig:
        configs.open_configuration(args.openConfig)
    elif args.printConfig:
        configs.print_configuration(args.printConfig)
    elif args.createConfig:
        configs.create_configuration(args.createConfig)
    elif args.deleteConfig:
        answer = input(f"Are you sure to delete {args.deleteConfig}? (y/n)")
        while answer != "y" and answer != "n":
            answer = input("Please enter \"y\" or \"n\" ")
        if answer == "y":
            configs.delete_configuration(args.deleteConfig)
    elif args.moveOneFile:
        file_path, config = tuple(args.moveOneFile)
        Mover(configs.get_config_path(config)).move_file(file_path, True)
    elif args.moveAllFilesInFolder:
        dir_path, config = tuple(args.moveAllFilesInFolder)
        Mover(configs.get_config_path(config)).move_files_in_dir(dir_path, True)


if __name__ == '__main__':
    main()
