# manuskript_md

A Python script to create Markdown-formatted text files from a [Manuskript](https://www.theologeek.ch/manuskript/) project.

## Features

- Creates *world.md*, a Markdown-formatted text file containing the story world descriptions. 
  The heading levels reflect the hierarchy in *Manuskript*. 
- Creates *characters.md*, a Markdown-formatted text file containing the character data.
  The first level headings show the characters' names. 
  The character information is structured on the second level.
- Creates *manuscript.md*, a Markdown-formatted text file containing all chapters and scenes.
- You can control which documents are created with the command line parameters. 

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [mskmd.py](https://raw.githubusercontent.com/peter88213/convert_manuskript-world/main/mskmd.py).

## Usage

You can start the script either from the command line, or 
from a batch file or shell script (that may launch *pandoc* afterwards). 

```
usage: mskmd.py [-h] [-m] [-w] [-c] projectdir

Create Markdown-formatted text files from a Manuscript project.

positional arguments:
  projectdir        The Manuskript project directory.

options:
  -h, --help        show this help message and exit
  -m, --manuscript  Create a "manuscript.md" file.
  -w, --world       Create a "world.md" file.
  -c, --characters  Create a "characters.md" file.

The created text files "manuscript.md", "world.md", and "characters.md" are
placed in the Manuskript project directory. If no option is selected, The
whole file set is created.
```

As a *Manuskript* user you probably have [pandoc](https://pandoc.org/) installed, 
so you can convert the Markdown-formatted text files into many other document formats, 
such as odt or docx. 

Here's how the command looks like for converting the *world.md* file into
*world.odt* for LibreOffice:

`pandoc -o world.odt -fMarkdown-smart world.md`




## License

Published under the [MIT License](https://opensource.org/licenses/mit-license.php)
