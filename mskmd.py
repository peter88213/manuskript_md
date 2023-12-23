#!/usr/bin/python3
"""mskmd.py

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

v1.0: Creating the new script.
v1.1: Add "shebang"; refactor.
v1.2: Fix a typo in the help text.
v2.0: Change the interface and convert the characters as well.
v2.1: Catch exceptions separately for characters and world.
v2.2: Refactor; fix messages.
v2.3: Fix a bug where character's multiline data gets lost; refactor.
v2.4: Use Unix line breaks for the Python script.
v3.0: New features: manuscript extraction, options.
v4.0: Change the interface and add summaries on all levels.
v4.1: Refactor the code: Reuse get_metadata with convert_characters. 
v4.2: Provide a main function to minimize the "script" part.
v4.3: Fix the "main" interface.
v4.4: Refactor.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/convert_manuskript_world
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import glob
import os

import xml.etree.ElementTree as ET

MAXLEVEL = 6
# Maximum chapter level.


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


def get_metadata(filePath):
    """Return a dictionary with metadata taken from a YAML-like file.

    Positional arguments:
        filePath: str -- Path to a YAML-like file.
    
    Raise an exception on error.    
    """
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    metadata = {}
    key = None
    data = []
    for line in lines:
        if line.startswith(' '):
            data.append(line.strip())
        elif ':' in line:
            if key:
                metadata[key] = '\n\n'.join(data)
                data = []
            key, value = line.split(':', maxsplit=1)
            data.append(value.strip())
        elif not line:
            break

    if key is not None:
        metadata[key] = '\n\n'.join(data)
    return metadata


def convert_characters(prjDir):
    """Create a Markdown file with project's character data.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """
    headings = [
        'Motivation',
        'Goal',
        'Conflict',
        'Epiphany',
        'Phrase Summary',
        'Paragraph Summary',
        ]

    charaLines = []
    for charaFile in glob.iglob(f'{prjDir}/characters/*.txt'):
        if charaFile is None:
            continue

        # Parse the YAML-like character data file.
        charaData = get_metadata(charaFile)

        charaLines.append(f"# {charaData.get('Name', 'Unknown')}")
        for heading in headings:
            if heading in charaData:
                charaLines.append(f'## {heading}')
                charaLines.append(charaData[heading])
    newFile = f'{prjDir}/characters.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(charaLines))
    return f'Markdown file "{os.path.normpath(newFile)}" written.'


def get_content(filePath):
    """Return a list with the scene content lines taken from a Manuskript scene file.
    
    Positional arguments:
        filePath: str -- Path to a Manuscript scene file.
    
    The Manuskript scene file consists of a YAML-like header, 
    a gap consisting of several blank lines, and a text body,
    consisting of paragraphs separated by single linebreaks.
    
    Raise an exception on error.        
    """
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    contentLines = []

    # Use a state machine to identify the text body.
    state = 0
    # 0=Header, 1=Gap between header and text body, 2=text body
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
    return contentLines


def convert_outline(prjDir):
    """Create Markdown files for all levels of the Manuskript outline.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a message on success. 
    Raise an exception on error.
    """

    def iter_dir(directory, level, maxLevel):
        level += 1
        if level > MAXLEVEL:
            raise ValueError(f'The maximum chapter level of {MAXLEVEL} has been exceeded.')

        entries = sorted(os.listdir(directory))
        for entry in entries:
            fullPath = os.path.join(directory, entry)
            if entry == ('folder.txt'):
                chapterMetadata = get_metadata(fullPath)
                chapterHeading = f"{'#' * level} {chapterMetadata.get('title', 'No title')}"

                # Manuscript heading.
                manuscript.append(chapterHeading)

                # Scene titles heading.
                scTitles.append(chapterHeading)

                # Full scene synopsis heading.
                scFullSynopsis.append(chapterHeading)

                # Short scene synopsis heading.
                scShortSynopsis.append(chapterHeading)

                # Full chapter synopsis.
                for i, chFullSynopsis in enumerate(chFullSynopses):
                    if level <= i:
                        chFullSynopses[i].append(chapterHeading)
                chFullSummaries = chapterMetadata.get('summaryFull', '')
                chFullSynopses[level].append(chFullSummaries)

                # Short chapter synopsis.
                for i, chShortSynopsis in enumerate(chShortSynopses):
                    if level <= i:
                        chShortSynopses[i].append(chapterHeading)
                chShortSummaries = chapterMetadata.get('summarySentence', '')
                chShortSynopses[level].append(chShortSummaries)

                if level > maxLevel:
                    maxLevel = level
                break

        for entry in entries:
            fullPath = os.path.join(directory, entry)
            if os.path.isdir(fullPath):
                maxLevel = iter_dir(fullPath, level, maxLevel)
            elif entry.endswith('.md'):
               sceneMetadata = get_metadata(fullPath)

               # Manuscript scene content.
               manuscript.append('\n\n'.join(get_content(fullPath)))

               # Scene titles.
               scTitle = sceneMetadata.get('title', 'No title')
               scTitles.append(scTitle)

               # Full scene synopsis.
               scLongSummaries = sceneMetadata.get('summaryFull', '')
               scFullSynopsis.append(scLongSummaries)

               # Short scene synopsis.
               scShortSummaries = sceneMetadata.get('summarySentence', '')
               scShortSynopsis.append(scShortSummaries)
        return maxLevel

    manuscript = []
    scTitles = []
    chFullSynopses = [ [] for _ in range(MAXLEVEL + 1) ]
    chShortSynopses = [ [] for _ in range(MAXLEVEL + 1) ]
    scFullSynopsis = []
    scShortSynopsis = []
    maxLevel = iter_dir(f'{prjDir}/outline', -1, 0)

    fileList = []
    manuscriptFile = f'{prjDir}/manuscript.md'
    with open(manuscriptFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(manuscript))
    fileList.append(os.path.normpath(manuscriptFile))

    scTitlesFile = f'{prjDir}/scene_titles.md'
    with open(scTitlesFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scTitles))
    fileList.append(os.path.normpath(scTitlesFile))

    scShortSynopsisFile = f'{prjDir}/short_scene_summaries.md'
    with open(scShortSynopsisFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scShortSynopsis))
    fileList.append(os.path.normpath(scShortSynopsisFile))

    scFullSynopsisFile = f'{prjDir}/full_scene_summaries.md'
    with open(scFullSynopsisFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scFullSynopsis))
    fileList.append(os.path.normpath(scFullSynopsisFile))

    for level, chShortSynopsis in enumerate(chShortSynopses):
        if level == 0:
            continue

        if level > maxLevel:
            break

        chShortSynopsisFile = f'{prjDir}/short_chapter_summaries_level_{level}.md'
        with open(chShortSynopsisFile, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(chShortSynopsis))
        fileList.append(os.path.normpath(chShortSynopsisFile))

    for level, chFullSynopsis in enumerate(chFullSynopses):
        if level == 0:
            continue

        if level > maxLevel:
            break

        chFullSynopsisFile = f'{prjDir}/full_chapter_summaries_level_{level}.md'
        with open(chFullSynopsisFile, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(chFullSynopsis))
        fileList.append(os.path.normpath(chFullSynopsisFile))

    output = '\n'.join(fileList)
    return f"Markdown file(s) written:\n{output}"


def main(prjDir, cnvOutline=True, cnvWorld=True, cnvCharacters=True):
    """Run conversion according to the arguments.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Optional arguments:
        cnvOutline: str -- If True, convert the story outline.
        cnvWorld: str -- If True, convert the story world data.
        cnvCharacters: str -- If True, convert the character data.
    
    Messages go to the console.
    """
    if cnvOutline:
        try:
            print(convert_outline(prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if cnvWorld:
        try:
            print(convert_world(prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if cnvCharacters:
        try:
            print(convert_characters(prjDir))
        except Exception as ex:
            print(f'ERROR: {str(ex)}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=f'Create Markdown-formatted text files from a Manuscript project.',
        epilog='The created text files are placed in the Manuskript project directory.')
    parser.add_argument('prjDir', metavar='projectdir',
                        help='The Manuskript project directory.')
    parser.add_argument('-o', '--outline', action='store_true',
                        help='Create markdown-formatted files for all levels of the Manuskript outline.')
    parser.add_argument('-w', '--world', action='store_true',
                        help='Create a "world.md" file.')
    parser.add_argument('-c', '--characters', action='store_true',
                        help='Create a "characters.md" file.')
    args = parser.parse_args()
    main(
        args.prjDir,
        cnvOutline=args.outline,
        cnvWorld=args.world,
        cnvCharacters=args.characters
        )

