from asr import ASR, Word, Punc

def punc_weights(words, factor=1.0, params=(2, 1.5, 0.9)):
    """
    Adjusts weights of punctuation.

    Takes:
    words: 1D list of Word tuples.
    params: tuple, weightmodifiers for the three
    most common interpunction symbols, default = (0.95, 0.85, 0.6)
    all other weightmodifiers were arbitrarily chosen.

    Outputs:
    words with adjusted weights.
    """

    period, question, comma = params
    for word in words:
        if type(word) == Punc:
            if word.text == '.':
                word.weight += period

            elif word.text == '?':
                word.weight += question

            elif word.text == ',':
                word.weight += comma

            elif word.text == '!':
                word.weight += 0.4

            elif word.text == ';' or word.text == ':':
                word.weight += 0.3

            else:
                word.weight += 0.2

    return words

data = ASR('asr/sample01.asrOutput.json').groups()
for w1, w2, in zip(data, punc_weights(data, params=(0.95, 0.85, 0.6))):
    print(w1.weight, w2.weight)