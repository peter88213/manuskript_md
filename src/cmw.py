#!/usr/bin/python3
"""Convert a Manuskript "world.opml" file into a Markdown file.

usage: cmw.py [-h] sourcefile

positional arguments:
  sourcefile  The path to the "world.opml" file.

options:
  -h, --help  show a help message and exit

The created text file "world.md" is placed in the same directory as the sourcefile.

v1.0: Creating the new script.
v1.1: Add "shebang"; refactor.
v1.2: Fix a typo in the help text.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/convert_manuskript_world
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
import os

import xml.etree.ElementTree as ET


def main(filePath):
    """Create a Markdown file with the contents of the input OPML file.
    
    Positional arguments:
        filePath: str -- The path to the "world.opml" file.
    
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

    body, extension = os.path.splitext(filePath)
    if extension.lower() != '.opml':
        raise ValueError(f'File must be of the OPML type, but is {extension}')

    xmlTree = ET.parse(filePath)
    lines = []
    xmlBody = xmlTree.getroot().find('body')
    if xmlBody is None:
        raise ValueError(f'"{filePath}" seems not to be a Manuscript world file.')

    convert_branch(xmlBody, 0)
    newFile = f'{body}.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(lines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f'Convert a Manuskript "world.opml" file into a Markdown-formatted text file.',
        epilog='The created text file "world.md" is placed in the same directory as the sourcefile.')
    parser.add_argument('filePath', metavar='sourcefile',
                        help='The path to the "world.opml" file.')
    args = parser.parse_args()
    try:
        print(main(args.filePath))
    except Exception as ex:
        print(f'ERROR: {str(ex)}')
