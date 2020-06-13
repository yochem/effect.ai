"""
This module provides functions to add weights to words in a caption. All
functions accept a List of Word or Punc classes and return the same type.
"""
from dataclasses import dataclass
from typing import List, Union

import nltk

import asr


@dataclass
class Pos(asr.Word):
    """
    Creates new dataclass for words with start time, end time and POS tag.
    """

    tag: str


def pos_tagger(words):
    """
    Get POS-tag dataclass from a Word or Punc dataclass.

    inputs:
    List of Words or Puncs tuples of the form:
        Word(<word>, <start time>, <end_time>) or
        Punc(<word>, <start time>, <end_time>)
        e.g: [Word(text="make", start_time=10.14, end_time=10.2, weight=1.0),
        Punc(text=".", start_time=10.25, end_time=10.25, weight=1.0)]

    outputs:
    Pos-tuple with added POS-tag of the form:
        Pos(<word>, <start time>, <end_time>)
        e.g: [Pos(text="make", start_time=10.14, end_time=10.2, weight=1.0,
        tag="VBD"), Pos(text=".", start_time=10.25, end_time=10.25,
        weight=1.0, tag=".")]]
    """
    tagged_words = []
    for word in words:
        text = word.text.lower()
        tag = nltk.pos_tag([text], tagset='universal')[0][1]

        tagged_words.append(Pos(word.text, word.start, word.end, word.weight,
                                tag=tag))

    return tagged_words


def pos_pron_verb(words, factor=1, split_weight=0.2):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between pronoun + verb

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'PRON' and next_word.tag == 'VERB':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_det_noun(words, factor=1, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between determiner + noun

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'DET' and next_word.tag == 'NOUN':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_prep_phrase(words, factor=1, split_weight=0.4):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between Preposition + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        words[index].weight += 1

        if word == tagged_words[-3]:
            next_word = tagged_words[index+1]
            nextnext = tagged_words[index+2]

            adp_options = (('ADP', 'DET', 'NOUN'),
                           ('ADP', 'ADJ', 'NOUN'),
                           ('ADP', 'PRON', 'NOUN'))
            if (word.tag, next_word.tag, nextnext.tag) in adp_options:
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


def pos_conj_phrase(words, factor=1, split_weight=0.3):
    """
    Adjust weight of word where split is not recommended:
        Avoid splitting between conjunction + following phrase

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    words: 1D list of Word tuples.
    split-weight: float indicating the importance of not splitting on the word.

    Output: 1D list of Word tuples with adjusted weights.
    """
    tagged_words = pos_tagger(words)

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


def speech_gaps(data: List[Union[asr.Word, asr.Punc]],
                threshold: float = 1.5) -> List[Union[asr.Word, asr.Punc]]:
    """
    Add weight to words with a speech gap after them. This function uses a
    threshold for the gap. The weight is hardcoded to be really high (100).
    """
    # loop pairwise over data
    for word_1, word_2 in zip(data, data[1:]):
        if word_2.start - word_1.end > threshold:
            word_1.weight = 100

    return data


def punctuation(words, factor=1.0, params=(0.95, 0.85, 0.6)):
    """
    Adjusts weights of punctuation.

    Takes:
    words: 1D list of Word tuples.
    params: tuple, weightmodifiers for the three
    most common punctuation symbols, default = (0.95, 0.85, 0.6)
    all other weightmodifiers were arbitrarily chosen.

    Outputs:
    words with adjusted weights.
    """
    period, question, comma = params

    punct_dict = {'.': period,
                  '?': question,
                  ',': comma,
                  '!': 0.4,
                  ';': 0.3,
                  ':': 0.3}

    for word in words:
        if isinstance(word, asr.Punc):
            word.weight += punct_dict.get(word.text, 0.2) * factor

    return words


def length(data, max_length=42, splits=[]):
    """
    Splits the data accordingly and finds the first space and makes the cut
    there. It does the same thing recursivly for words that are left in the
    sentence.
    """
    if sum([len(x) for x in data]) <= 42:
        splits.append(data)
        return splits

    sentence = ' '.join(data)
    while sentence[max_length] != ' ':
        max_length -= 1

    splits.append(sentence[:max_length].split())
    length(sentence[max_length:].split(), splits=splits)
    return splits


def split_length(data, factor=1, max_length=42):
    """
    Takes the datastructure as input and outputs the same datastructure with
    the changed weights according to a 42 character limit.
    """
    sentence = [word.text for word in data]
    splits = length(sentence, max_length=max_length)

    number = 0
    for split in splits:
        number += len(split)
        data[number].weight += 1 * factor
        data[number-1].weight += 0.5 * factor
        data[number-2].weight += 0.25 * factor

    return data
