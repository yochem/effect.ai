from typing import List, Union

from asr import Punc, Word


def speech_gaps(data: List[Union[Word, Punc]],
                threshold: int = 1) -> List[List[Union[Word, Punc]]]:
    """
    Split *transcript* into caption groups using time difference between words.

    This uses a threshold (given in seconds). Returns Caption with caption
    groups.
    """
    result = []
    caption_group = []

    # loop pairwise over data
    for w1, w2 in zip(data, data[1:]):
        caption_group.append(w1)

        if w2.start - w1.end > threshold:
            result.append(caption_group)
            caption_group = [w2]

    return result
