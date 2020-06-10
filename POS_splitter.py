from asr import ASR
from pos_tagger import basic_pos, no_apos, basic_words_pos, Pos

def pos_splitter_pron_verb(words, split_weight=0.2):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between pronoun + verb

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    1D list of Word objects.
    Split-weight indicating the importance of not-splitting on the word.

    Output: 1D list of Word objects with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]

        if word.tag == 'PRON' and next_word.tag == 'VERB':
            words[index].weight = words[index].weight - split_weight

    return words

def pos_splitter_det_noun(words, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between determiner + noun

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    1D list of Word objects.
    Split-weight indicating the importance of not-splitting on the word.

    Output: 1D list of Word objects with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]

        # Determiner and Noun
        if word.tag == 'DET' and next_word.tag == 'NOUN':
            words[index].weight = words[index].weight - split_weight

    return words


def pos_splitter_prep_phrase(words, split_weight=0.4):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between Preposition + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    1D list of Word objects.
    Split-weight indicating the importance of not-splitting on the word.

    Output: 1D list of Word objects with adjusted weights.
    """
    tagged_words = basic_words_pos(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        nextnext = tagged_words[index+2]
        nextnextnext = tagged_words[index+3]

    	# Preposition and phrase
        if word.tag == 'ADP' and ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next_word.tag == 'DET' and nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
            words[index].weight = words[index].weight - split_weight

    return words

def pos_splitter_conj_phrase(tagged_words, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between conjunction + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    1D list of Word objects.
    Split-weight indicating the importance of not-splitting on the word.

    Output: 1D list of Word objects with adjusted weights.
    """
    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        nextnext = tagged_words[index+2]
        nextnextnext = tagged_words[index+3]

        # Conjuction and phrase
        if word.tag == 'CONJ' and ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or
        (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next_word.tag == 'DET' and
        nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or
        (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
            words[index].weight = words[index].weight - split_weight

    return words

data = ASR('asr/sample01.asrOutput.json').groups()
