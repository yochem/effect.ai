from asr import ASR
from time_gaps import speech_gaps
from punc_split import punc_weights
from POS_splitter import pos_splitter_pron_verb
from POS_splitter import pos_splitter_det_noun
from POS_splitter import pos_splitter_prep_phrase
from POS_splitter import pos_splitter_conj_phrase
from caption import write


def split_weights(caption, result=[], max_chars: int = 84):
    if len(' '.join(x.text for x in caption)) <= max_chars:
        result.append(caption)
        return result

    max_weight = max(caption[5:-5], key=lambda t: t.weight)
    max_index = caption.index(max_weight)
    split_weights(caption[:max_index+1])
    split_weights(caption[max_index+1:])

    return result


def main(subs):
    subs = speech_gaps(subs)
    subs = punc_weights(subs)
    subs = pos_splitter_pron_verb(subs)
    subs = pos_splitter_det_noun(subs)
    subs = pos_splitter_prep_phrase(subs)
    subs = pos_splitter_conj_phrase(subs)

    groups = split_weights(subs)

    write(groups, 'videos/sample01.srt')


if __name__ == '__main__':
    data = ASR('asr/sample01.asrOutput.json').groups()
    main(data)
