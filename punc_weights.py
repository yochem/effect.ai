from asr import Punc

def punc_weights(words, factor=1.0, params=(2, 1.5, 0.9)):
    """
    Adjusts weights of punctuation.

    Takes:
    words: 1D list of Word tuples.
    params: tuple, weightmodifiers for the three
    most common punctuation symbols, default = (0.95, 0.85, 0.6)
    all other weightmodifiers were arbitrarily chosen.

    Outputs:
    words with adjusted weights.
    """

    period, question, comma = params
    for word in words:
        if isinstance(word, Punc):
            if word.text == '.':
                word.weight += period * factor

            elif word.text == '?':
                word.weight += question * factor

            elif word.text == ',':
                word.weight += comma * factor

            elif word.text == '!':
                word.weight += 0.4 * factor

            elif word.text == ';' or word.text == ':':
                word.weight += 0.3 * factor

            else:
                word.weight += 0.2 * factor

    return words
