"""
The ASR module.

Module for working with ASR (Automatic Speech Recognition) files formatted as
JSON. It provides the ASR() class and the Word() and Punc() dataclasses.
"""
from dataclasses import dataclass
import json
from typing import List, Union


@dataclass
class Word:
    """
    Basic word data. Containing the word the start time of the word, end time
    of the word and the splitting weight.
    """
    text: str
    start: float
    end: float
    weight: float


@dataclass
class Punc(Word):
    """
    Basic punctuation data. Start and end time are kept for flexibility using
    both Word() and Punc() together. This dataclass is used to simplify
    recognising punctuation in the caption.
    """


class ASR:
    """
    This class helps working with ASR files. It provides an API for loading
    these files and converting it to varias datastructures.
    """

    def __init__(self, filename: str):
        """Load asr file with given filename. Returns JSON object."""
        with open(filename, 'r') as f:
            raw = f.read()

        self.data = json.loads(raw)

    def transcript(self) -> str:
        """Return the transcript as one big string."""
        return self.data['results']['transcripts'][0]['transcript']

    def json(self) -> dict:
        """Return the full JSON file as python dictionary."""
        return self.data

    def groups(self) -> List[Union[Word, Punc]]:
        """
        Convert the ASR to the following format to a list of Word() and
        Punc()'s. The Word() and Punc() are dataclasses containing the textual
        representation and the start and end time.
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
