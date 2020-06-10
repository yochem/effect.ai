"""
This is where the magic happens.
"""
from asr import ASR
import caption
from error_function import basic_error
from split_length import split_length
from time_gaps import speech_gaps


def train(data_name):
    data = ASR(data_name).groups()

    data = speech_gaps(data)

    caption.write(data, 'videos/sample01.srt')


if __name__ == '__main__':
    train('asr/sample01.asrOutput.json')
