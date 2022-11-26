# file-mover

An open source file manager CLI that enables moving files based on file properties and specified criteria.
![](../../Downloads/fmover_demo.gif)
## Description
Tired of moving files manually? Given a file path and a configuration, file-mover will move files based on the specified criteria.

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
If a file was downloaded from www.uni.com and the file name contains the word "Analysis", the file will be moved to the folder "/Users/user/Documents/Uni".

If a file extension is ".pdf", the file will be moved to the folder "/Users/user/Documents/PDF".

Further information on the configuration is given in the chapter "Configuration".


## Getting Started




### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)