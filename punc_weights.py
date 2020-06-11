from asr import Punc


def punc_weights(words, factor=1.0, params=(0.95, 0.85, 0.6)):
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

    punct_dict = {'.': period,
                  '?': question,
                  ',': comma,
                  '!': 0.4,
                  ';': 0.3,
                  ':': 0.3}

    for word in words:
        if isinstance(word, Punc):
            word.weight += punct_dict.get(word.text, 0.2) * factor

    return words
