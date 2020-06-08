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
    text: str
    start: float
    end: float


@dataclass
class Punc:
    text: str
    start: float
    end: float


class ASR():
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
        Convert the ASR to the following format:
        [
            [
                Word(),
                Word(),
                Punc()
            ],
            [Word(), Word(), Punc()],
            ...
        ]
        where the outer list is the complete caption, the inner lists are
        caption groups and the Word() and Punc() are dataclasses containing
        the textual representation and the start and end time.
        """
        cap: List[Union[Word, Punc]] = []

        words = self.data['results']['items']

        for word in words:
            text = word['alternatives'][0]['content']

            if word['type'] == 'pronunciation':
                start = word['start_time']
                end = word['end_time']
                cap.append(Word(text, float(start), float(end)))
            else:
                time = cap[-1].end
                cap.append(Punc(text, time, time))

        return cap


if __name__ == '__main__':
    a = ASR('asr/sample01.asrOutput.json')
    print(a.groups())
