#!/usr/bin/python3
"""mskmd.py

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

v1.0: Creating the new script.
v1.1: Add "shebang"; refactor.
v1.2: Fix a typo in the help text.
v2.0: Change the interface and convert the characters as well.
v2.1: Catch exceptions separately for characters and world.
v2.2: Refactor; fix messages.
v2.3: Fix a bug where character's multiline data gets lost; refactor.
v2.4: Use Unix line breaks for the Python script.
v3.0: New features: manuscript extraction, options.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/convert_manuskript_world
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
import glob
import os

import xml.etree.ElementTree as ET


def convert_world(prjDir):
    """Create a Markdown file with the project's story world data.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """

    def iter_branch(xmlBranch, level):
        level += 1
        for xmlNode in xmlBranch.iterfind('outline'):
            lines.append(f"{'#' * level} {xmlNode.attrib.get('name', 'Element')}")
            desc = xmlNode.attrib.get('description', '').replace('\n', '\n\n')
            lines.append(desc)
            iter_branch(xmlNode, level)

    filePath = f'{prjDir}/world.opml'

    # Parse the OPML world file.
    xmlTree = ET.parse(filePath)
    xmlBody = xmlTree.getroot().find('body')
    if xmlBody is None:
        raise ValueError(f'"{filePath}" seems not to be a Manuskript world file.')

    lines = []
    iter_branch(xmlBody, 0)
    newFile = f'{prjDir}/world.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(lines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


def convert_characters(prjDir):
    """Create a Markdown file with project's character data.
    
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

        # Parse the YAML-like character data file.
        heading = ''
        for line in lines:
            if line.startswith(' '):
                text = line
                appendParagraph = True
            elif ':' in line:
                heading, text = line.split(':', maxsplit=1)
                appendParagraph = False
            else:
                continue

            if heading in headings:
                text = text.strip()
                if text:
                    if appendParagraph:
                        newlines.append(text)
                    elif heading == 'Name':
                        newlines.append(f'# {text}')
                    else:
                        newlines.append(f'## {heading}')
                        newlines.append(text)
    newFile = f'{prjDir}/characters.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(newlines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


def convert_manuscript(prjDir):
    """Create a Markdown file with the project's chapters and scenes.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """

    def get_title(filePath):
        with open(filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines[0].split(':', maxsplit=1)[1].strip()

    def get_content(filePath):
        with open(filePath, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        contentLines = []
        state = 0
        # 0=Header, 1=Gap between header and body, 2=body
        for line in lines:
            if state == 2:
                contentLines.append(line)
            elif state == 0:
                if not line:
                    state = 1
            elif state == 1:
                if line:
                    state = 2
                    contentLines.append(line)
        return '\n\n'.join(contentLines)

    def iter_dir(directory, level):
        level += 1
        entries = sorted(os.listdir(directory))
        for entry in entries:
            fullPath = os.path.join(directory, entry)
            if entry == ('folder.txt'):
                heading = get_title(fullPath)
                newlines.append(f"{'#' * level} {heading}")
                break
        for entry in entries:
            fullPath = os.path.join(directory, entry)
            if os.path.isdir(fullPath):
                iter_dir(fullPath, level)
            elif entry.endswith('.md'):
               newlines.append(get_content(fullPath))

    newlines = []
    iter_dir(f'{prjDir}/outline', -1)
    newFile = f'{prjDir}/manuscript.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(newlines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f'Create Markdown-formatted text files from a Manuscript project.',
        epilog='The created text files "manuscript.md", "world.md", and "characters.md" are placed \
        in the Manuskript project directory. \
        If no option is selected, The whole file set is created.')
    parser.add_argument('prjDir', metavar='projectdir',
                        help='The Manuskript project directory.')
    parser.add_argument('-m', '--manuscript', action='store_true',
                        help='Create a "manuscript.md" file.')
    parser.add_argument('-w', '--world', action='store_true',
                        help='Create a "world.md" file.')
    parser.add_argument('-c', '--characters', action='store_true',
                        help='Create a "characters.md" file.')
    args = parser.parse_args()
    if not (args.manuscript or args.world or args.characters):
        convertAll = True
    else:
        convertAll = False
    if convertAll or args.manuscript:
        try:
            print(convert_manuscript(args.prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if convertAll or args.world:
        try:
            print(convert_world(args.prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if convertAll or args.characters:
        try:
            print(convert_characters(args.prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
