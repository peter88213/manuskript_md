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
v5.0: API change: The converter routines return lists of the created Markdown files' paths.
v5.0.1: Refactor.
v5.0.2: Refactor: One text file reader fits all.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/manuskript_md
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
    
    Return a list containing the Markdown file path on success. 
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
    return [newFile]


def get_data(filePath):
    """Return a tuple with metadata and contents from a Manuskript text file.
    
    First element: A dictionary with metadata taken from any YAML-like Manuskript file.
    Second element: A list with the scene content lines taken from a Manuskript scene file.
    
    Positional arguments:
        filePath: str -- Path to a Manuskript text file.
    
    The Manuskript scene file consists of a YAML-like header, 
    a gap consisting of several blank lines, and a text body,
    consisting of paragraphs separated by single linebreaks.
    Other Manuskript data files, such as the character data
    or the folder data, only have the YAML-like header.
    
    Raise an exception on error.        
    """
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    contentLines = []
    metadataLines = []
    metadata = {}
    key = None

    # Use a state machine to identify the text body.
    state = 0
    # 0=Header, 1=Gap between header and text body, 2=text body
    for line in lines:
        if state == 2:
            contentLines.append(line)
        elif state == 0:
            if line.startswith(' '):
                metadataLines.append(line.strip())
            elif ':' in line:
                if key:
                    metadata[key] = '\n\n'.join(metadataLines)
                    metadataLines = []
                key, value = line.split(':', maxsplit=1)
                metadataLines.append(value.strip())
            elif not line:
                if key:
                    metadata[key] = '\n\n'.join(metadataLines)
                state = 1
        elif state == 1:
            if line:
                state = 2
                contentLines.append(line)
    return metadata, contentLines


def convert_characters(prjDir):
    """Create a Markdown file with project's character data.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a list containing the Markdown file path on success. 
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
        charaData, __ = get_data(charaFile)

        charaLines.append(f"# {charaData.get('Name', 'Unknown')}")
        for heading in headings:
            if heading in charaData:
                charaLines.append(f'## {heading}')
                charaLines.append(charaData[heading])
    newFile = f'{prjDir}/characters.md'
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(charaLines))
    return [newFile]


def convert_outline(prjDir):
    """Create Markdown files for all levels of the Manuskript outline.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Return a list containing the Markdown file paths on success. 
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

                # Read the chapter metadata file.
                chapterMetadata, __ = get_data(fullPath)
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
                        chFullSynopsis.append(chapterHeading)
                chFullSummaries = chapterMetadata.get('summaryFull', '')
                chFullSynopses[level].append(chFullSummaries)

                # Short chapter synopsis.
                for i, chShortSynopsis in enumerate(chShortSynopses):
                    if level <= i:
                        chShortSynopsis.append(chapterHeading)
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

                # Read the Manuscript scene file.
                sceneMetadata, sceneLines = get_data(fullPath)
                manuscript.append('\n\n'.join(sceneLines))

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
    fileList.append(manuscriptFile)

    scTitlesFile = f'{prjDir}/scene_titles.md'
    with open(scTitlesFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scTitles))
    fileList.append(scTitlesFile)

    scShortSynopsisFile = f'{prjDir}/short_scene_summaries.md'
    with open(scShortSynopsisFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scShortSynopsis))
    fileList.append(scShortSynopsisFile)

    scFullSynopsisFile = f'{prjDir}/full_scene_summaries.md'
    with open(scFullSynopsisFile, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(scFullSynopsis))
    fileList.append(scFullSynopsisFile)

    for level, chShortSynopsis in enumerate(chShortSynopses):
        if level == 0:
            continue

        if level > maxLevel:
            break

        chShortSynopsisFile = f'{prjDir}/short_chapter_summaries_level_{level}.md'
        with open(chShortSynopsisFile, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(chShortSynopsis))
        fileList.append(chShortSynopsisFile)

    for level, chFullSynopsis in enumerate(chFullSynopses):
        if level == 0:
            continue

        if level > maxLevel:
            break

        chFullSynopsisFile = f'{prjDir}/full_chapter_summaries_level_{level}.md'
        with open(chFullSynopsisFile, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(chFullSynopsis))
        fileList.append(chFullSynopsisFile)

    return fileList


def main(prjDir, cnvOutline=True, cnvWorld=True, cnvCharacters=True):
    """Run conversion according to the arguments.
    
    Positional arguments:
        prjDir: str -- The Manuskript project directory.
    
    Optional arguments:
        cnvOutline: bool -- If True, convert the story outline.
        cnvWorld: bool -- If True, convert the story world data.
        cnvCharacters: bool -- If True, convert the character data.
    
    Messages go to the console.
    """
    if cnvOutline:
        try:
            fileList = convert_outline(prjDir)
            for filePath in fileList:
                print(f"Markdown file written: {os.path.normpath(filePath)}")
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if cnvWorld:
        try:
            fileList = convert_world(prjDir)
            print(f"Markdown file written: {os.path.normpath(fileList[0])}")
        except Exception as ex:
            print(f'ERROR: {str(ex)}')
    if cnvCharacters:
        try:
            fileList = convert_characters(prjDir)
            print(f"Markdown file written: {os.path.normpath(fileList[0])}")
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

