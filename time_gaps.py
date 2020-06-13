from typing import List, Union

from asr import Punc, Word


def speech_gaps(data: List[Union[Word, Punc]],
                threshold: float = 1.5) -> List[Union[Word, Punc]]:
    """
    Add weight to words with a speech gap after them. This function uses a
    threshold for the gap. The weight is hardcoded to be really high (100).
    """
    # loop pairwise over data
    for w1, w2 in zip(data, data[1:]):
        if w2.start - w1.end > threshold:
            w1.weight = 100

    return data
