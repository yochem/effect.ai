"""
This is where the magic happens.
"""
import caption
from asr import ASR

data = ASR('asr/sample01.asrOutput.json').groups()
