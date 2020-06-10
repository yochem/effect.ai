from datetime import timedelta
from typing import List, Union

import srt

from asr import Word, Punc


# Type alias for our datastructure
Caption = List[List[Union[Word, Punc]]]


def create_subtitles(caption: Caption) -> List[srt.Subtitle]:
    """
    Create a list of srt.Subtitle subtitles. Ready for composing to a string.
    """
    subtitles = []
    for i, group in enumerate(caption):
        text = ' '.join(word.text for word in group)
        start = group[0].start
        end = group[-1].end
        sub = srt.Subtitle(i, timedelta(seconds=start),
                           timedelta(seconds=end), text)
        subtitles.append(sub)

    return subtitles


def write(caption: Caption, filename: str) -> None:
    """
    Compose the caption using the function above and write to file with given
    filename.
    """
    composed = srt.compose(create_subtitles(caption))

    with open(filename, 'w') as f:
        f.write(composed)
