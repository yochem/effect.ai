from asr import ASR
from pos_tagger import basic_words_pos


def pos_splitter_pron_verb(words, factor=1, split_weight=0.2):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between pronoun + verb

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'PRON' and next_word.tag == 'VERB':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_splitter_det_noun(words, factor=1, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between determiner + noun

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'DET' and next_word.tag == 'NOUN':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_splitter_prep_phrase(words, factor=1, split_weight=0.4):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between Preposition + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        words[index].weight += 1

        if word == tagged_words[-3]:
            next_word = tagged_words[index+1]
            nextnext = tagged_words[index+2]

            if word.tag == 'ADP' and \
                ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or
                 (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or
                 (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
                words[index].weight -= split_weight * (1 / factor)

            continue

        if word == tagged_words[-2]:
            continue

        next_word = tagged_words[index+1]
        nextnext = tagged_words[index+2]
        nextnextnext = tagged_words[index+3]

        if word.tag == 'ADP' and \
            ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or
             (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or
             (next_word.tag == 'DET' and nextnext.tag == 'ADJ' and
              nextnextnext.tag == 'NOUN') or
             (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
            words[index].weight -= split_weight * (1 / factor)

    return words

def pos_splitter_conj_phrase(words, factor=1, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between conjunction + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        words[index].weight += 1

        if word == tagged_words[-3]:
            next_word = tagged_words[index+1]
            nextnext = tagged_words[index+2]

            if word.tag == 'CONJ' and \
                ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or
                 (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or
                 (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
                words[index].weight -= split_weight * (1 / factor)

            continue

        if word == tagged_words[-2]:
            continue

        next_word = tagged_words[index+1]
        nextnext = tagged_words[index+2]
        nextnextnext = tagged_words[index+3]

        if word.tag == 'CONJ' and \
            ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or
             (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or
             (next_word.tag == 'DET' and nextnext.tag == 'ADJ' and
              nextnextnext.tag == 'NOUN') or
             (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
            words[index].weight -= split_weight * (1 / factor)

    return words


if __name__ == '__main__':
    data = ASR('asr/sample01.asrOutput.json').groups()
    print(pos_splitter_conj_phrase(data, factor=2))
