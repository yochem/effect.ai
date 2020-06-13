from typing import List, Union

import srt

from asr import ASR, Word, Punc
import caption
import weighting


Caption = List[Union[Word, Punc]]
Groups = List[Caption]


def basic_error(input_subs: List[srt.Subtitle],
                manual_subs: List[srt.Subtitle],
                max_width: int = 42) -> int:
    """
    Takes the generated subtitles and the manual subtitles and compares
    them. A caption group is considered to be correct if the last word of the
    caption group and the first word of the next are the same as in the manual
    subtitles. When max_width is exceeded we penalise the captiongroup. In the
    end this function is intended to be maximalised.

    takes:
    input_subs: the generated subtitles as a srt parsed list
    manual_subs: the man-made subtitles we considered to correct
    max_width: how long a caption is allowed to be, default 42, 0 means no
    restrictions

    outputs: amount of correctly created captiongroups, and amount of times
    max_width was exceeded
    """
    good = 0
    penalty = 0
    for i, (sub1, next_sub1) in enumerate(zip(input_subs, input_subs[1:])):
        for sub2, next_sub2 in zip(manual_subs[i:], manual_subs[i+1:]):
            if sub1.content.split()[-1] == sub2.content.split()[-1] and \
               next_sub1.content.split()[0] == next_sub2.content.split()[0]:
                good += 1
                break

        if max_width and len(sub1.content) > max_width:
            penalty += 1

    return -(good - penalty)


def split_weights(subs: Caption, result: Groups = [],
                  max_chars: int = 84) -> Groups:
    if len(' '.join(x.text for x in subs)) <= max_chars:
        result.append(subs)
        return result

    max_weight = max(subs[5:-5], key=lambda t: t.weight)
    max_index = subs.index(max_weight)
    split_weights(subs[:max_index+1])
    split_weights(subs[max_index+1:])

    return result


def create_groups(subs: Caption) -> Groups:
    subs = weighting.speech_gaps(subs)
    subs = weighting.punctuation(subs)
    subs = weighting.pos_pron_verb(subs)
    subs = weighting.pos_det_noun(subs)
    subs = weighting.pos_prep_phrase(subs)
    subs = weighting.pos_conj_phrase(subs)

    return split_weights(subs)


if __name__ == '__main__':
    DATA = ASR('../asr/sample01.asrOutput.json').groups()
    GROUPS = create_groups(DATA)
    caption.write(GROUPS, 'videos/sample01.srt')
