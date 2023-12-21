# convert_manuskript_world

A Python script to convert the *Manuskript* world and character files into markdown.

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [cmw.py](https://raw.githubusercontent.com/peter88213/convert_manuskript-world/main/src/cmw.py).

## Usage

You can start the script either from the command line, e.g. `python3 cmw.py <path-to-project-dir>`, 
from a batch file or shell script (that may launch *pandoc* afterwards), 
or via dragging your Manuskript project folder icon and dropping it on the *cmw.py* icon. 

```
command: cmw.py [-h] projectdir

positional arguments:
  projectdir  The Manuskript project directory.

options:
  -h, --help  show this help message and exit

```

The created text files "world.md" and "characters.md" are placed in the
Manuskript project directory.

## License

Published under the [MIT License](https://opensource.org/licenses/mit-license.php)
