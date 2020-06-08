import json
import nltk
import numpy as np

def no_apos(tokenized_text):
    """Concatenates splitted word contractions from a POS-tagged text
    together. Concatenated word keeps tag from first word of concatination.

    Input: Tokenized and POS-tagged text as 1D-list of tuples.

    Output: Tokenized and POS-tagged text as 1D-list of tuples with contractions
            together as one word.
    """

    i=1

    while i != len(tokenized_text):

        if "'" in tokenized_text[i][0]:

            tokenized_text[i-1] = list(tokenized_text[i-1])
            tokenized_text[i-1][0] = tokenized_text[i-1][0] + tokenized_text[i][0]
            tokenized_text[i-1] = tuple(tokenized_text[i-1])
            tokenized_text.remove(tokenized_text[i])

        i += 1

    return tokenized_text


# TODO: language feature
def basic_pos(asrfile, lang='eng', sents=True, split_apos=False):
    """
    Converts the transcript of an amazon-generated asr file to a pos-tagged list

    inputs:
    asrfile: file name of the amazon-generated asr file
    sents: tokenize each sentence before tagging, recommended by nltk
    split_apos: If 'False' does not split word contractions e.g. "we're" or
                "hadn't". Standard keeps tag from first word of contraction.

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
        if split_apos:
            for sent in nltk.sent_tokenize(text):
                words.append(nltk.word_tokenize(sent))

            return nltk.pos_tag_sents(words)
        else:
            for sent in nltk.sent_tokenize(text):
                words.append(no_apos(nltk.pos_tag(nltk.word_tokenize(sent))))
            return words

    if split_apos:
        return nltk.pos_tag(nltk.word_tokenize(text))

    return no_apos(nltk.pos_tag(nltk.word_tokenize(text)))


print(basic_pos('asr/sample01.asrOutput.json'))
