from asr import ASR
data = ASR('asr/sample01.asrOutput.json').groups()

print(len(data))
# print(data[:20])
"""
Input: list of words
"""
