"""
Functions to convert our dataformat (Caption) to various formats used by the
srt package.
"""
from datetime import timedelta
import re
from typing import List, Union

import srt

import asr


# Type alias
Caption = List[List[Union[asr.Word, asr.Punc]]]


def create_subtitles(caption: Caption) -> List[srt.Subtitle]:
    """
    A srt.Subtitle instance is made for every caption group, with the start
    time from the first element in the capture group and the end time of the
    last element in the capture group.
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


def compose(caption: Caption) -> str:
    """Convert subtitles to the content of a srt file as a string."""
    return srt.compose(create_subtitles(caption))


def write(caption: Caption, filename: str) -> None:
    """
    Compose the caption using the function above and write to file with given
    filename.
    """
    composed = srt.compose(create_subtitles(caption))

    with open(filename, 'w') as f:
        f.write(composed)
