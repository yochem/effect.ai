"""
The ASR module.

Module for working with ASR (Automatic Speech Recognition) files formatted as
JSON. It provides the ASR() class.
"""
from collections import namedtuple
import json

Word = namedtuple('Word', 'text start end')
Punc = namedtuple('Punc', 'text start end')


class ASR():
    def __init__(self, filename: str):
        """Load asr file with given filename. Returns JSON object."""
        with open(filename, 'r') as f:
            raw = f.read()

        self.data = json.loads(raw)

    def json(self):
        """Return the full JSON file as python dictionary."""
        return self.data

    def groups(self):
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
        caption groups and the Word() and Punc() are namedtuples containing
        the textual representation and the start and end time.
        """
        caption = []

        words = self.data['results']['items']

        for word in words:
            text = word['alternatives'][0]['content']

            if word['type'] == 'pronunciation':
                start = word['start_time']
                end = word['end_time']
                caption.append(Word(text, start, end))
            else:
                time = caption[-1].end
                caption.append(Punc(text, time, time))

        return caption


if __name__ == '__main__':
    a = ASR('asr/sample01.asrOutput.json')
    print(a.groups())
