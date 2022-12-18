import pytest
import fmover.cli as cli
import json
import os


@pytest.fixture(scope="session")
def temp_files_dir(tmp_path_factory):
    temp_files_dir = tmp_path_factory.mktemp("files")
    temp_files_dir.joinpath("Magma.txt").touch()
    temp_files_dir.joinpath("China.txt").touch()
    temp_files_dir.joinpath("China.jpeg").touch()
    temp_files_dir.joinpath("Mount Everest.jpeg").touch()
    return temp_files_dir


@pytest.fixture(scope="session")
def temp_config_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("configurations", False)


def generate_config(temp_config_dir, command=[{"FILE_EXTENSION(.jpeg) & NAME(*)": "NAME(*)"}],
                    where_from={"wiki": "./Library"},
                    name={"China": "./Countries", "Mount Everest": "./Mountains"},
                    file_extension={".jpeg": "./Home"}):
    test_config_path = temp_config_dir / "test_config.json"
    with open(test_config_path, "w") as test_config:
        json.dump({"COMMAND": command,
                   "WHERE_FROM": where_from,
                   "NAME": name,
                   "FILE_EXTENSION": file_extension}, test_config, indent=2)
    return test_config_path


def test_list(capsys, temp_config_dir):
    test_config = generate_config(temp_config_dir)
    cli.main(["-c", str(temp_config_dir), "list"])
    captured = capsys.readouterr()

    assert captured.out == f"{os.path.splitext(test_config.name)[0]}\n"
    assert captured.err == ""


def test_print(capsys, temp_config_dir):
    test_config = generate_config(temp_config_dir)
    cli.main(["-c", str(temp_config_dir), "print", os.path.splitext(test_config.name)[0]])
    captured = capsys.readouterr()

    assert captured.out == f"{json.dumps(json.load(open(test_config, 'r')), indent=2)}\n"
    assert captured.err == ""


def test_create_config(temp_config_dir):
    cli.main(["-c", str(temp_config_dir), "create", "test_create"])
    assert os.path.exists(str(temp_config_dir / "test_create.json"))


def test_delete_config(temp_config_dir):
    test_config = generate_config(temp_config_dir)
    assert os.path.exists(str(test_config))
    cli.main(["-c", str(temp_config_dir), "delete", os.path.splitext(test_config.name)[0]])
    assert not os.path.exists(str(test_config))


def test_move_all(temp_files_dir, temp_config_dir):
    test_config = generate_config(temp_config_dir)
    cli.main(["-c", str(temp_config_dir), "move-all", "-f", str(temp_files_dir), os.path.splitext(test_config.name)[0]])
    print(os.listdir(temp_files_dir))
    assert os.path.exists(temp_files_dir / "Countries" / "China.jpeg")
    assert os.path.exists(temp_files_dir / "Mountains" / "Mount Everest.jpeg")
    assert not os.path.exists(temp_files_dir / "Library")
    assert not os.path.exists(temp_files_dir / "Home")
