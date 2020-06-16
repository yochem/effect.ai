"""Automatic Speech Recognition module.

This Module is for working with ASR (Automatic Speech Recognition) files
formatted as JSON. It provides the ASR class and the Word and Punc
dataclasses.

Example:
    >>> import asr
    >>> asr.ASR('/path/to/file.json').groups()
    [Word(text='An', start=0, end=1, weight=0),
     Word(text='example', start=1, end=2, weight=0),
     Punc(text='.', start=2, end=2, weight=0)]
"""
from dataclasses import dataclass
import json
from typing import List, Union


@dataclass
class Word:
    """Python representation of a word from the ASR file.

    Basic data of a spoken word.

    Attributes:
        text: The transcripted word.
        start: Begin time of the word in seconds.
        end: End time of the word in seconds.
        weight: How good a split after this word would be. How higher the
            value, the better the split would be.
    """
    text: str
    start: float
    end: float
    weight: float


@dataclass
class Punc(Word):
    """Python representation of punctuation from the ASR file.

    Basic data of a punctuation mark.

    Attributes:
        text: The punctuation character.
        start: End time of the word before the punctuation in seconds.
        end: End time of the word before the punctuation in seconds.
        weight: How good a split after this word would be. How higher the
            value, how better the split would be.
    """


class ASR:
    """Automatic Speech Recognition class.

    This class helps working with ASR files. It provides an API for loading
    these files and converting it to various datastructures.

    Attributes:
        data: All data from the ASR file loaded with the JSON module.
    """

    def __init__(self, filename: str):
        """Load asr file with given filename.

        Args:
            filename: A string of an ASR filename.
        """
        with open(filename, 'r') as f:
            raw = f.read()

        self.data = json.loads(raw)

    def transcript(self) -> str:
        """Return the transcript as one big string.

        Returns:
            A string containing the whole transcript.
        """
        return self.data['results']['transcripts'][0]['transcript']

    def json(self) -> dict:
        """Return the full JSON file as python dictionary.

        Returns:
            A dictionary containing the transcript and all words with times
            and precision rates. For full overview of what this returns, see
            the contents of ../asr/sample01.asrOutput.json.
        """
        return self.data

    def groups(self) -> List[Union[Word, Punc]]:
        """Convert the ASR to the following format to the Caption-list format:

            [Word(text='An', start=0, end=1, weight=0),
             Word(text='example', start=1, end=2, weight=0),
             Punc(text='.', start=2, end=2, weight=0)]

        Returns:
            Caption-list with weights initialised at 0.
        """
        cap = []

        words = self.data['results']['items']

        for word in words:
            text = word['alternatives'][0]['content']

            if word['type'] == 'pronunciation':
                start = word['start_time']
                end = word['end_time']
                cap.append(Word(text, float(start), float(end), weight=0))
            else:
                time = cap[-1].end
                cap.append(Punc(text, time, time, weight=0))

        return cap
