"""
Part-Of-Speech Tagger.

This file contains the dataclass Pos and a function to POS-tag Word objects.
"""
from dataclasses import dataclass

import nltk

from asr import Word


@dataclass
class Pos(Word):
    """
    Creates new dataclass for words with start time, end time and POS tag.
    """

    tag: str


def basic_words_pos(words):
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
