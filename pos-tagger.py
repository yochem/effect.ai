import json
import nltk
import numpy as np


# TODO: language feature
def basic_pos(asrfile, lang='eng', sents=True):
    """
    Converts the transcript of an amazon-generated asr file to a pos-tagged list

    inputs:
    asrfile: file name of the amazon-generated asr file
    sents: tokenize each sentence before tagging, recommended by nltk

    outputs:
    a list of tuples of the form: [(<word>, <tag>), ...],
    e.g.: [('the', 'DT'), ...]
    """
    with open(asrfile) as asrOutput:
        data = json.load(asrOutput)

    # 'transcripts' is a list with one dictionary that holds the transcript
    text = data['results']['transcripts'][0]['transcript']

    if sents:
        words = []
        for sent in nltk.sent_tokenize(text):
            words.append(nltk.word_tokenize(sent))

        return nltk.pos_tag_sents(words)

    return nltk.pos_tag(nltk.word_tokenize(text))


pos = basic_pos('asr/sample01.asrOutput.json')
flat = [word for sent in pos for word in sent]
print(len(flat))
# print(flat[:20])
