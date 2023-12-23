# manuskript_md

A Python script to create Markdown-formatted text files from a [Manuskript](https://www.theologeek.ch/manuskript/) project.

## Features

- Creates *world.md*, a Markdown-formatted text file containing the story world descriptions. 
  The heading levels reflect the hierarchy in *Manuskript*. 
- Creates *characters.md*, a Markdown-formatted text file containing the character data.
  The first level headings show the characters' names. 
  The character information is structured on the second level.
- Creates *manuscript.md*, a Markdown-formatted text file containing all chapters and scenes.
- Creates synopses on all levels (up to 6) of the Manuskript *Outline*:
    - Full chapter summaries in a document per chapter level.
    - Short chapter summaries in a document per chapter level.
    - Full scene summaries.
    - Short scene summaries.
    - Scene titles.
- You can control which documents are created with the command line parameters. 

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [mskmd.py](https://raw.githubusercontent.com/peter88213/manuskript_md/main/mskmd/mskmd.py).

## Usage

You can start the script either from the command line, or 
from a batch file or shell script (that may launch *pandoc* afterwards). 

```
usage: mskmd.py [-h] [-o] [-w] [-c] projectdir

Create Markdown-formatted text files from a Manuscript project.

positional arguments:
  projectdir        The Manuskript project directory.

options:
  -h, --help        show this help message and exit
  -o, --outline     Create markdown-formatted files for all levels of the
                    Manuskript outline.
  -w, --world       Create a "world.md" file.
  -c, --characters  Create a "characters.md" file.

The created text files are placed in the Manuskript project directory.
```

As a *Manuskript* user you probably have [pandoc](https://pandoc.org/) installed, 
so you can convert the Markdown-formatted text files into many other document formats, 
such as odt or docx. 

Here's how the command looks like for converting the *world.md* file into
*world.odt* for LibreOffice:

`pandoc -o world.odt -fMarkdown-smart world.md`




## License

Published under the [MIT License](https://opensource.org/licenses/mit-license.php)
