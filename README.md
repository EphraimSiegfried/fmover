
<div align="center">
<br>
  <h1> fmover </h1>
  <i> An open source file manager CLI that enables moving files based on file properties and specified criteria.
</i>
  <br>
  <br>
  <p align="center">
    <img src="https://github.com/EphraimSiegfried/fmover/actions/workflows/tests.yml/badge.svg">
    <img src="https://img.shields.io/badge/Available-on%20PyPi-blue?logoColor=white&logo=Python">
    <img src="https://img.shields.io/badge/Python-3.6%2B-blue?logo=python">
    <img src="https://img.shields.io/badge/Formatting-Black-black.svg">
  </p>
    <p align="center">
      <img src="https://user-images.githubusercontent.com/114060741/204161513-aaa94afc-9ed0-48ef-9ce1-053d0d6eab8d.gif" alt="A demo of fmover moving files in a directory">
  </p>
</div>

## Description
fmover is an open source file management command line interface that makes it easy to automatically move files based on their properties and specific criteria. With fmover, you can move files based on their source, extension, and name by specifying these properties in a configuration file. This allows you to quickly and easily organize your files without having to manually move them yourself. Plus, fmover is compatible with Python 3.6 and higher and is available on PyPi for easy installation. With a simple configuration file, you can easily specify where to move your files and fmover will do the rest. Streamline your file organization and save time with fmover.


## Getting Started
### Dependencies
You need to have at least Python 3.6 installed on your system. You can download it from [here](https://www.python.org/downloads/).

The extended file attribute "WHERE_FROM" which stores where the file was downloaded/obtained from is currently only available on macOS.
If you are on another operating system, you can still use the program but you will not be able to use the this property.


### Installing
Install with pip:
```shell
pip install fmover
```

### Usage


To get an overview of the available commands, run:
```shell
fmover -h
```

#### Editing, creating and deleting configurations
You will have a default configuration file once you install the program.

To list all available configurations, run:
```shell
fmover list
```

To print the content of a configuration file, run:
```shell
fmover print your_config_name
```

To create a new configuration file, run:
```shell
fmover create new_config
```
To open and eventually edit a configuration file in your default text editor, run:
```shell
fmover open your_config_name
```

To delete a configuration file, run:
```shell
fmover delete your_config_name
```

#### Moving files
To move one file based on the configuration, run:
```shell
fmover move /path/to/file your_config_name
```

To move all files in a directory based on the configuration, run:
```shell
fmover move-all /path/to/directory your_config_name
```

To get a pop-up notification when files are moved, run:
```shell
fmover move-all /path/to/directory your_config_name --notify
```

To create destination folders if they do not exist, run:
```shell
fmover move-all /path/to/directory your_config_name --force
```

To only get the information where the files would be moved without actually moving them, run:
```shell
fmover move-all /path/to/directory your_config_name --dry-run
```

### The configuration
fmover uses a JSON configuration file to specify which file properties and patterns should be used to trigger file movements. The file is divided into four sections: COMMAND, WHERE_FROM, NAME, and FILE_EXTENSION.

Here is an example configuration file:

```json
{
  "COMMAND": [
    {"NAME(Analysis) & WHERE_FROM(www.uni.com)": "WHERE_FROM(www.uni.com)"}, 
    {"FILE_EXTENSION(*)": "FILE_EXTENSION(*)"}
  ],
  "WHERE_FROM": {
    "www.uni.com": "/Users/user/Documents/Uni",
    "www.uni2.com": "/Users/user/Documents/Uni2"
  },
  "NAME": {
    "Analysis": "/Users/user/Documents/Uni/Analysis"
  },
  "FILE_EXTENSION": {
    ".pdf": "/Users/user/Documents/PDF",
    ".docx": "/Users/user/Documents/DOCX",
    ".pptx": "/Users/user/Documents/PPTX"
  }
}
```
#### COMMAND
This section specifies the conditions that must be met in order for a file to be moved. The format is a list of dictionaries, with each dictionary representing a command. Each command consists of an antecedent (left side of the command) and a consequent (right side of the command).

The antecedent is a combination of tokens, separated by conjunction (&). Each token is a file property and pattern, formatted as PROPERTY(PATTERN). If a file property matches the specified pattern, the token is considered true.

The consequent is a file property and pattern, formatted as PROPERTY(PATTERN). If the antecedent is true, the file will be moved to the destination specified by the consequent.

#### WHERE_FROM, NAME, and FILE_EXTENSION

These sections specify the file properties and patterns that can be used in the COMMAND section. Each section is a dictionary, with the keys being the patterns and the values being the destinations for the files. If a file property matches the specified pattern, it will be moved to the corresponding destination.

#### Example
In the above configuration, the first command states that if a file has the name "Analysis" and was obtained from "www.uni.com", it should be moved to the folder "/Users/user/Documents/Uni". The second command states that if a file has any extension defined in FILE_EXTENSION, it should be moved to the corresponding destination specified in the FILE_EXTENSION section (e.g. a pptx file would be moved to /Users/user/Documents/PPTX).


## Automator Folder Action on macOS
On macOs, you can combine the program with the Automator Folder Action to automatically move files to the correct folder when they are downloaded.
To do this, follow these steps:
1. Open Automator.
2. Click on "New Document".
3. Select "Folder Action" and click "Choose".
4. At "Folder action receives files and folders added to:" select the folder you want to monitor.
5. At the library on the left, search for "Run Shell Script" and double click it.
6. At the "Shell" field, select "pass input as arguments".
7. Paste the following code into your terminal and copy the output:
```shell
echo "for f in"' "$@"' "\ndo\n    $(which fmover) move"' "$f" default'"\ndone"
```
8. Paste the output into the "Shell" field.
9. Replace "default" with the name of your configuration.
10. Save the action.

Each time a file is added to the folder, the action will be executed and the file will be moved to the correct folder.

## Help

<strong>"WHERE_FROM" doesn't work on my mac. What can I do?</strong>

Your Browser might not store any information about where a file was downloaded from.
To find out if your browser stores this information, download a file and then run the following command in your terminal:
```shell
xattr -p com.apple.metadata:kMDItemWhereFroms /path/to/downloaded/file
```
If the command returns nothing, your browser does not store this information. If it returns something, it does.

I know that it works on Chrome. If you know if it works on other browsers, please let me know.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [filejuggler](https://www.filejuggler.com/features/move-and-copy-files-automatically/)
* [notify-py](https://github.com/ms7m/notify-py)
