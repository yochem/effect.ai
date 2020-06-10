from datetime import timedelta
from typing import List, Union

import srt

from asr import ASR, Word, Punc


# Type alias
Caption = List[List[Union[Word, Punc]]]


def compose(caption: Caption) -> str:
    """
    Compose a SRT string. A srt.Subtitle instance is made for every caption
    group, with the start time from the first element in the capture group and
    the end time of the last element in the capture group. A list of these
    subtitles is then composed using the srt.compose() function.
    """
    subtitles = []
    for i, group in enumerate(caption):
        text = ' '.join(word.text for word in group)
        start = group[0].start
        end = group[-1].end
        sub = srt.Subtitle(i, timedelta(start), timedelta(end), text)
        subtitles.append(sub)

    return srt.compose(subtitles)


def write(caption: Caption, filename: str) -> None:
    """
    Compose the caption using the function above and write to file with given
    filename.
    """
    composed = compose(caption)

    with open(filename, 'w') as f:
        f.write(composed)


if __name__ == '__main__':
    data = ASR('asr/sample01.asrOutput.json').groups()
    print(compose([data]))
