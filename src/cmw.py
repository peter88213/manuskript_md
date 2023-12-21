"""Create Markdown-formatted text files from the Manuskript world and characters files.

usage: crmd.py [-h] projectdir

positional arguments:
  projectdir  The Manuskript project directory.

options:
  -h, --help  show this help message and exit

The created text files "world.md" and "characters.md" are placed in the
Manuskript project directory.

v1.0: Creating the new script.
v1.1: Add "shebang"; refactor.
v1.2: Fix a typo in the help text.
v2.0: Change the interface and convert the characters as well.
v2.1: Catch exceptions separately for characters and world.
v2.2: Refactor; fix messages.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/convert_manuskript_world
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
import glob
import os

import xml.etree.ElementTree as ET


def convert_world(prjDir):
    """Create a Markdown file with the contents of the project's "world.opml" file.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """

    def convert_branch(xmlBranch, level):
        level += 1
        for xmlNode in xmlBranch.iterfind('outline'):
            lines.append(f"{'#' * level} {xmlNode.attrib.get('name', 'Element')}")
            desc = xmlNode.attrib.get('description', '').replace('\n', '\n\n')
            lines.append(desc)
            convert_branch(xmlNode, level)

    filePath = f'{prjDir}/world.opml'
    xmlTree = ET.parse(filePath)
    lines = []
    xmlBody = xmlTree.getroot().find('body')
    if xmlBody is None:
        raise ValueError(f'"{filePath}" seems not to be a Manuskript world file.')

    convert_branch(xmlBody, 0)
    newFile = f'{prjDir}/world.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(lines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


def convert_characters(prjDir):
    """Create a Markdown file with the contents of project's "characters" files.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """
    headings = [
        'Name',
        'Motivation',
        'Goal',
        'Conflict',
        'Epiphany',
        'Phrase Summary',
        'Paragraph Summary',
        ]

    newlines = []
    for charaFile in glob.iglob(f'{prjDir}/characters/*.txt'):
        if charaFile is None:
            continue

        with open(charaFile, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines:
            for heading in headings:
                if line.startswith(heading):
                    text = line.split(f'{heading}:', maxsplit=1)[1].strip()
                    if text:
                        if heading == 'Name':
                            newlines.append(f'# {text}')
                        else:
                            newlines.append(f'## {heading}')
                            newlines.append(text)
                    break
    newFile = f'{prjDir}/characters.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(newlines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f'Create Markdown-formatted text files from the Manuskript world and characters files.',
        epilog='The created text files "world.md" and "characters.md" are placed in the Manuskript project directory.')
    parser.add_argument('prjDir', metavar='projectdir',
                        help='The Manuskript project directory.')
    args = parser.parse_args()
    try:
        print(convert_world(args.prjDir))
    except Exception as ex:
        print(f'ERROR: {str(ex)}')
    try:
        print(convert_characters(args.prjDir))
    except Exception as ex:
        print(f'ERROR: {str(ex)}')
