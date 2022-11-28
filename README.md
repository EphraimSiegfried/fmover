
<div align="center">
<br>
  <h1> fmover </h1>
  <i> An open source file manager CLI that enables moving files based on file properties and specified criteria.
</i>
  <br>
  <br>
    <p align="center">
      <img src="https://user-images.githubusercontent.com/114060741/204161513-aaa94afc-9ed0-48ef-9ce1-053d0d6eab8d.gif" alt="A demo of fmover moving files in a directory">
  </p>
</div>

## Description
Tired of moving files manually? Given a file path and a configuration, fmover will move files based on the specified criteria.

The program can currently move files based on the properties: file source, file extension and file name. 
These properties are specified in the configuration which is a json file.

An example configuration looks like this:
```json
  {
  "COMMAND": [
    {"NAME(Analysis) & WHERE_FROM(www.uni.com)": "WHERE_FROM(www.uni.com)"}, 
    {"WHERE_FROM(*)": "WHERE_FROM(*)"}
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
The command section specifies which properties and respective patterns should be considered and where to move a file if that file has those properties. (e.g. the first command in natural language would be: "If a file has the name Analysis and was obtained from www.uni.com, move it to /Users/user/Documents/Uni").
The remaining sections specify which properties and patterns to consider.

Some examples of what the program will do with the configuration above:
* If a file was downloaded from www.uni.com and the file name contains the word "Analysis", the file will be moved to the folder "/Users/user/Documents/Uni".
* If a file extension is ".pdf", the file will be moved to the folder "/Users/user/Documents/PDF".

Further information on the configuration is given in the section [The Configuration](# The Configuration).


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
fmover -l
```

To print the content of a configuration file (in this example the default configuration), run:
```shell
fmover -p default
```

To create a new configuration file, run:
```shell
fmover -n new_config
```
To open and eventually edit a configuration file in your default text editor, run:
```shell
fmover -o new_config
```

To delete a configuration file, run:
```shell
fmover -d new_config
```

#### Moving files
To move one file based on the configuration (in this example the default configuration), run:
```shell
fmover -m /path/to/file default 
```

To move all files in a directory based on the configuration (in this example the default configuration), run:
```shell
fmover -a /path/to/directory default 
```

To move files without a pop-up notification, run:
```shell
fmover -a /path/to/directory default -s
```

To create destination folders if they do not exist, run:
```shell
fmover -a /path/to/directory default -f
```

### The configuration
The configuration defines what properties to consider and how to move files based on those properties. 
There are Commands and Properties. Commands specify which properties to consider and where to move a file if it has those properties.
A property specifies which patterns to consider and where to move a file if it has those patterns.

#### Commands
* The configuration must have the outer key "COMMAND" with a value which is a list of singleton dictionaries. 
These singleton dictionaries are commands which consist of antecedents (as keys) and consequents (as values).
* An antecedent consist of tokens which are seperated by "&". A consequent only has one token.
* Tokens consist of a parameter and a pattern. The tokens have the following form: "PARAMETER(PATTERN)".
The parameter can be one of the following: "NAME", "FILE_EXTENSION", "WHERE_FROM".
The pattern can be a string or a wildcard "*". A wildcard matches any pattern in the respective property.
* If the parameter is declared in the command it must be a property in the config.

This is an example of a valid command section:
```json
  {
  "COMMAND": [
    {
      "NAME(Tests) & FILE_EXTENSION(.pdf) & WHERE_FROM(www.uni.com": "NAME(Tests)"
    },
    {
      "WHERE_FROM(*)": "WHERE_FROM(*)"
    }
  ]
  }
```

#### Properties
* The configuration can have (it's optional) the outer keys "NAME", "FILE_EXTENSION" and "WHERE_FROM" with values which are dictionaries.
* The keys of these dictionaries are patterns and the values are paths.

This is an example of a valid property section:
```json
  {
  "NAME": {
    "Tests": "/Users/user/Documents/Tests",
    "Analysis": "/Users/user/Documents/Analysis"
  },
  "FILE_EXTENSION": {
    ".pdf": "/Users/user/Documents/PDF",
    ".docx": "/Users/user/Documents/DOCX",
    ".pptx": "/Users/user/Documents/PPTX"
  },
  "WHERE_FROM": {
    "www.uni.com": "/Users/user/Documents/Uni",
    "www.uni2.com": "/Users/user/Documents/Uni2"
  }
}
```
#### Example Behavior
Let us merge these two sections to get a full configuration:
```json
  {
  "COMMAND": [
    {
      "NAME(Tests) & FILE_EXTENSION(.pdf) & WHERE_FROM(www.uni.com": "NAME(Tests)"
    },
    {
      "WHERE_FROM(*)": "WHERE_FROM(*)"
    }
  ],
  "NAME": {
    "Tests": "/Users/user/Documents/Tests",
    "Analysis": "/Users/user/Documents/Analysis"
  },
  "FILE_EXTENSION": {
    ".pdf": "/Users/user/Documents/PDF",
    ".docx": "/Users/user/Documents/DOCX",
    ".pptx": "/Users/user/Documents/PPTX"
  },
  "WHERE_FROM": {
    "www.uni.com": "/Users/user/Documents/Uni",
    "www.uni2.com": "/Users/user/Documents/Uni2"
  }
}
```
Now let us consider the following file:
* The file name is "Tests_Algebra".
* The file extension is ".pdf".
* The file was downloaded from "www.uni.com".

In the antecedent of the first command, all tokens are satisfied.
Therefore, the consequent of the first command is executed. 
The consequent is "NAME(Tests)". This means that the file will be moved to the value of the key "Tests" in the property "NAME".
In this case, the file will be moved to "/Users/user/Documents/Tests".

Now let us consider the following file:
* The file name is "Test".
* The file extension is ".pdf".
* The file was downloaded from "www.uni.com".

In the antecedent of the first command, the first token is not satisfied, because "Test" does not contain "Tests".
Therefore, the consequent of the first command is not executed.
The antecedent of the second command is satisfied, because there exists a pattern in the property "WHERE_FROM" which matches with where the file was obtained from.
Therefore, the consequent of the second command is executed and the file will be moved to the value of the pattern "www.uni.com" in the property "WHERE_FROM", which is "/Users/user/Documents/Uni".

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
echo "for f in"' "$@"' "\ndo\n    $(which fmover) -m"' "$f" default'"\ndone"
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
