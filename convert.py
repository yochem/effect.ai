"""
This is where the magic happens.
"""
from asr import ASR

data = ASR('asr/sample01.asrOutput.json').groups()
