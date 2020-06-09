from asr import ASR
from pos_tagger import basic_pos, no_apos, basic_word_pos, Pos


def pos_splitter(tagged_data):
    """

    Merges word groups that cannot be split to one Word.
        tag them with str 'No split'

    Input: 1D list of Words.

    Output: 1D list with words merged that cannot be split.
    """

    for index, word in enumerate(tagged_data):

        next = tagged_data[index+1]

        if word.tag == 'DT' and next.tag == 'NN':

            tagged_data[index].tag = 'No split'
            tagged_data[index].text = word.text + " " + next.text
            tagged_data[index].end = next.end

            tagged_data.remove(next)

    return tagged_data


data = ASR('asr/sample01.asrOutput.json').groups()

"""Create new list of words with POS-tags"""
tagged_words = []

for i in range(len(data)):
    tagged_words.append(basic_word_pos(data[i]))

# Voorbeeld
lijst = [Pos(text='a', start='902.52', end='902.71', tag='DT'),
Pos(text='very', start='902.72', end='903.29', tag='NN'),
Pos(text='viable', start='903.46', end='904.04', tag='DT'),
Pos(text='gaming',start='904.04', end='904.35', tag='NN')]

print(pos_splitter(lijst))
