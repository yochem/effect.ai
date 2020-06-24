"""
This module provides functions to add weights to words in a caption. All
functions accept a List of Word or Punc classes and return the same type.
"""
from dataclasses import dataclass
import re
from typing import List, Union, Sequence
import math

import nltk

from . import asr


Caption = List[Union[asr.Word, asr.Punc]]


@dataclass
class Pos(asr.Word):
    """Part-Of-Speech-Tag dataclass.

    Has same attributes as Word with additional POS-tag attribute.

    Attributes:
        text: See Word dataclass documentation.
        start: See Word dataclass documentation.
        end: See Word dataclass documentation.
        weight: See Word dataclass documentation.
        tag: Part-Of-Speech tag assigned to a word.

    """
    tag: str


def pos_tagger(words: Caption) -> List[Pos]:
    """Tagging Caption elements with Part-Of-Speech tags.

    Returns a universal POS-tagged list of the custom Caption-list dataformat
    using the NLTK library function pos_tag().

    When tagging with the pos_tag() function, the optional parameter 'tagset'
    is set to 'universal' to simplify tags.

    See https://www.nltk.org/book/ch05.html for documentation.

    Args:
        words: The custom Caption-list dataformat.

    Returns:
        The Caption-list with added universal POS-tags.
    """
    tagged_words = []
    for word in words:
        text = word.text.lower()
        tag = nltk.pos_tag([text], tagset='universal')[0][1]

        tagged_words.append(Pos(word.text, word.start, word.end, word.weight,
                                tag=tag))

    return tagged_words


def pos_pron_verb(words: Caption, factor: float = 1,
                  split_weight: float = 0.2) -> Caption:
    """Avoid splitting between pronoun + verb by adjusting weight.

    Returns the custom Caption-list dataformat with adjusted weights for the
    elements in the Caption-list where split is not recommended according to
    one of the BBC subtitle guidelines.

    For documentation of the guidelines see:
        https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Args:
        words: The custom POS-tagged Caption-list dataformat.
        factor: Float indicating the importance of this split function.
        split_weight: Float indicating the importance of not splitting on the
            word.

    Returns:
        The custom POS-tagged Caption-list dataformat with adjusted weight
        attribute.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'PRON' and next_word.tag == 'VERB':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_det_noun(words: Caption, factor: float = 1,
                 split_weight: float = 0.3) -> Caption:
    """Avoid splitting between determiner + noun by adjusting weight.

    Returns the custom Caption-list dataformat with adjusted weights for the
    elements in the Caption-list where split is not recommended according to
    one of the BBC subtitle guidelines.

    For documentation of the guidelines see:
        https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Args:
        words: The custom POS-tagged Caption-list dataformat.
        factor: Indicating the importance of this split function.
        split_weight: Indicating the importance of not splitting on the
            word.

    Returns:
        The custom POS-tagged Caption-list dataformat with adjusted weight
        attribute.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'DET' and next_word.tag == 'NOUN':
            words[index].weight -= split_weight * (1 / factor)

    return words


def pos_prep_phrase(words: Caption,
                    factor: float = 1,
                    split_weight: float = 0.4) -> Caption:
    """Avoid splitting between preposition + following phrase.

    Returns the custom Caption-list dataformat with adjusted weights for the
    elements in the Caption-list where split is not recommended according to
    one of the BBC subtitle guidelines.

    For documentation of the guidelines see:
        https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Args:
        words: The custom POS-tagged Caption-list dataformat.
        factor: Indicating the importance of this split function.
        split_weight: Indicating the importance of not splitting on the
            word.

    Returns:
        The custom POS-tagged Caption-list dataformat with adjusted weight
        attribute.
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


def pos_conj_phrase(words: Caption,
                    factor: float = 1,
                    split_weight: float = 0.3) -> Caption:
    """Avoid splitting between conjunction + following phrase.

    Returns the custom Caption-list dataformat with adjusted weights for the
    elements in the Caption-list where split is not recommended according to
    one of the BBC subtitle guidelines.

    For documentation of the guidelines see:
        https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Args:
        words: The custom POS-tagged Caption-list dataformat.
        factor: Indicating the importance of this split function.
        split_weight: Indicating the importance of not splitting on the
            word.

    Returns:
        The custom POS-tagged Caption-list dataformat with adjusted weight
        attribute.
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


def complex_verbs(words: Caption, factor: float = 1,
                  split_weight: float = 0.3) -> Caption:
    """Avoid splitting between complex verbs # BUG: y adjusting weight.

    Returns the custom Caption-list dataformat with adjusted weights for the
    elements in the Caption-list where split is not recommended according to
    one of the BBC subtitle guidelines.

    For documentation of the guidelines see:
        https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Args:
        words: The custom POS-tagged Caption-list dataformat.
        factor: Indicating the importance of this split function.
        split_weight: Indicating the importance of not splitting on the
            word.

    Returns:
        The custom POS-tagged Caption-list dataformat with adjusted weight
        attribute.
    """
    tagged_words = pos_tagger(words)

    for index, word in enumerate(tagged_words[:-1]):
        next_word = tagged_words[index+1]
        words[index].weight += 1

        if word.tag == 'VERB' and next_word.tag == 'VERB':
            words[index].weight -= split_weight * (1 / factor)

    return words



def speech_gaps(data: Caption, threshold: float = 1.5) -> Caption:
    """Add weight to words with a speech gap after them.

    This function uses a threshold for the gap. The weight is hardcoded to be
    really high (100).

    Args:
        data: The transcript subtitles according to our custom Caption-list
            datastructure.
        threshold: Determines the length of a speech gap.

    Returns:
        The Caption-list datastructure with adjusted weights.
    """
    # loop pairwise over data
    for word_1, word_2 in zip(data, data[1:]):
        if word_2.start - word_1.end > threshold:
            word_1.weight = 100

    return data


def punctuation(words: Caption,
                factor: float = 1,
                params: Sequence[float] = (0.95, 0.85, 0.6)) -> Caption:
    """Adjusts weights of punctuation.

    Args:
        words: The transcript subtitles according to our custom Caption-list
            datastructure.
        factor: Indicating the importance of this split function.
        params: Weightmodifiers for the three most common punctuation symbols,
            default = (0.95, 0.85, 0.6) all other weightmodifiers were
            arbitrarily chosen.

    Returns:
        The Caption-list datastructure with adjusted weights.
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


def length(data: List[str],
           max_length: int = 42,
           splits: List[List[str]] = []) -> List[List[str]]:
    """
    Splits the data accordingly and finds the first space and makes the cut
    there. It does the same thing recursivly for words that are left in the
    sentence.

    Args:
        data: A list containing multiple strings
        max_length: A character limit of 84 or 42 characters
        splits: At first an empty list that would be filled recursively with
            multiple lists with each containing multiple strings

    Returns:
        A list containing multiple lists with each containing multiple strings.
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


def split_length(data: Caption,
                 factor: float = 1,
                 max_length: int = 42) -> Caption:
    """
    Adjusts the weights of words according to a character limit of either 84 or
    42 characters. The words that needs adjusting are determined by the
    function length.

    Args:
        data: With a character limit of 84 it takes the transcript subtitles
            according to our custom Caption-list datastructure. With a 42
            character limit it takes a caption group according to our custom
            Caption-list datastructure.
        factor: Indicating the importance of this split function.
        max_length: A character limit of 84 or 42 characters.

    Returns:
        The Caption-list datastructure with adjusted weights.
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


def _abs_linspace(start: int, stop: int, step: int) -> List[float]:
    """Simple version of np.abs(np.linspace())."""
    if step == 1:
        return [start]

    return [abs(start + x * (stop-start)/(step - 1)) for x in range(step)]


def line_breaks(groups: List[Caption], factor: float = 1,
                bound: int = 42) -> List[Caption]:
    r"""Add line breaks to caption groups.

    This function appends the string '\n' to the word in the middle of the
    caption group with the highest weight, if the caption is longer than
    <bound> characters (usually 42).

    First, a list of split options is created. This makes sure both lines are
    shorter than <bound> characters. Then it add weights to these split options
    using numpy's linspace over a parabola with roots at the number of split
    options: \(-\frac{1}{h^2}x^2 + 1\).

    Args:
        groups: The caption groups, consists of a list of our custom
            Caption-list dataformats.
        factor: Giving extra (or less) weight to the function's weights.
        bound: The maximal length of a line.

    Returns:
        The caption groups, consists of a list of our custom Caption-list
        dataformats.
    """
    f = lambda x, h: -1 / (h**2) * x**2 + 1
    line_in_bound = lambda s: len(' '.join(x.text for x in s)) <= bound

    for group in groups:
        # don't split caption groups with fewer characters than bound
        sent = ' '.join(w.text for w in group)
        punc = re.compile(r' ([,.?!])')
        sent = punc.sub(r'\g<1>', sent)

        if len(sent) <= bound:
            continue

        goods = []

        for i, _ in enumerate(group):
            if line_in_bound(group[:i]) and line_in_bound(group[i:]):
                goods.append(group[i-1])

        # if there's no 'right' split, just split in half
        if len(goods) == 0:
            group[len(group)//2].text += '\n'
            continue

        half = math.ceil(len(goods) / 2)
        weights = _abs_linspace(-half, half, len(goods) + 2)[1:-1]

        for word, weight in zip(goods, weights):
            word.weight += f(weight, half) * factor

        split = max(goods, key=lambda t: t.weight)
        split.text += '\n'

    return groups
