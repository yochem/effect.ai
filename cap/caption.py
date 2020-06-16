"""
Module to convert our Caption dataformat to various srt package formats.
"""
from datetime import timedelta
import re
from typing import List, Union

import srt

from . import asr


# Type aliases
Caption = List[Union[asr.Word, asr.Punc]]
Groups = List[Caption]


def create_subtitles(caption: Groups) -> List[srt.Subtitle]:
    """
    A srt.Subtitle instance is made for every caption group, with the start
    time from the first element in the caption group and the end time of the
    last element in the caption group.

    Args:
        caption: The caption groups, consists of a list of our custom
            Caption-list dataformats.

    Returns:
        List of srt.Subtitle instances, created from the caption groups.
    """
    punc = re.compile(r' ([,.?!])')

    subtitles = []
    for i, group in enumerate(caption):
        text = ' '.join(word.text for word in group)

        # strip spaces in front of punctuation
        text = punc.sub(r'\g<1>', text)

        start = group[0].start
        end = group[-1].end
        sub = srt.Subtitle(i, timedelta(seconds=start),
                           timedelta(seconds=end), text)
        subtitles.append(sub)

    return subtitles


def compose(caption: Groups) -> str:
    """
    Convert caption groups to the content of a srt file as a string.

    Args:
        caption: The caption groups, consists of a list of our custom
            Caption-list dataformats.

    Returns:
        A formatted srt file as a string.
    """
    return srt.compose(create_subtitles(caption))


def write(caption: Groups, filename: str) -> None:
    """
    Writes a srt file from the caption groups using the srt.compose() function.
    Writes to a file with the given filename.

    Args:
        caption: The caption groups, consists of a list of our custom
            Caption-list dataformats.
        filename: Name of the file to write the srt file to. Filename is
            recommended to end with '.srt'.
    """
    composed = srt.compose(create_subtitles(caption))

    with open(filename, 'w') as f:
        f.write(composed)
