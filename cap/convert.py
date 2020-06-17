"""
The convert module.

Module for converting the input data, consisting of words with time stamps and
POS-tags, to caption groups.  The error between the created output and the
manual-subtitles can also be measured by basic_error.
"""

from typing import List, Union

import srt

from . import asr
from . import caption
from . import weighting


Caption = List[Union[asr.Word, asr.Punc]]
Groups = List[Caption]


def basic_error(input_subs: List[srt.Subtitle],
                manual_subs: List[srt.Subtitle],
                max_width: int = 42) -> int:
    """
    Takes the generated subtitles and the manual subtitles and compares
    them. A caption group is considered to be correct if the last word of the
    caption group and the first word of the next are the same as in the manual
    subtitles. When max_width is exceeded we penalise the captiongroup.
    When there is a difference in the amount of caption groups, this is also a penalty.
    In the end this function is intended to be maximalised.

    Args:
        input_subs: The generated subtitles as a srt parsed list.
        manual_subs: The man-made subtitles we considered to correct.
        max_width: How long a caption is allowed to be, default 42, 0 means no
            restrictions.

    Returns:
        Amount of correctly created caption groups minus amount of times
        max_width was exceeded minus the difference in the amount of caption groups.
    """
    good = 0
    penalty = 0
    amount_input = 0
    amount_manual = 0

    for sub in zip(input_subs):
        amount_input += 1
    for sub in zip(manual_subs):
        amount_manual += 1
    amount_difference = amount_input - amount_manual

    for i, (sub1, next_sub1) in enumerate(zip(input_subs, input_subs[1:])):
        for sub2, next_sub2 in zip(manual_subs[i:], manual_subs[i+1:]):
            if sub1.content.split()[-1] == sub2.content.split()[-1] and \
               next_sub1.content.split()[0] == next_sub2.content.split()[0]:
                good += 1
                break

        if max_width and len(sub1.content) > max_width:
            penalty += 1
    return -(good - penalty - amount_difference*0.4)


def split_weights(subs: Caption, result: Groups = [],
                  max_chars: int = 84) -> Groups:
    """
    Function that splits the input data based on the highest weights.
    Recursively go trough the input data and split at the word after the
    highest weight. For every caption group created is checked if the caption
    group doesn't exceed the maximum characters. If it doesn't exceed the
    maximum characters, append the caption group to the result list.

    Args:
        subs: The caption-list with added weights.
        result: Empty list for the caption groups.
        max_chars: Maximal number of characters for one caption group, which is
            standard 84.

    Returns:
        List that contains the caption groups.
    """
    if len(' '.join(x.text for x in subs)) <= max_chars:
        result.append(subs)
        return result

    max_weight = max(subs[5:-5], key=lambda t: t.weight)
    max_index = subs.index(max_weight)
    split_weights(subs[:max_index+1])
    split_weights(subs[max_index+1:])

    return result


def create_groups(subs: Caption) -> Groups:
    """
    Function that first adds the weights to the words in the caption-list and
    then uses the split_weight function to create caption groups. Adding
    weight is done by using the functions for adding weight in weighting.py.
    They are listed in order of importance. Now that the words have weights,
    the function split_weight can be used to create the caption groups.

    Args:
        subs: Input data without weighting.

    Returns:
        List that contains the caption groups.
    """
    subs = weighting.speech_gaps(subs)
    subs = weighting.punctuation(subs)
    subs = weighting.pos_pron_verb(subs)
    subs = weighting.pos_det_noun(subs)
    subs = weighting.pos_prep_phrase(subs)
    subs = weighting.pos_conj_phrase(subs)

    return split_weights(subs)


if __name__ == '__main__':
    DATA = asr.ASR('../asr/sample01.asrOutput.json').groups()
    GROUPS = create_groups(DATA)
    caption.write(GROUPS, 'videos/sample01.srt')
