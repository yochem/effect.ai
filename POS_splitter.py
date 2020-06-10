from asr import ASR
from pos_tagger import basic_pos, no_apos, basic_word_pos, Pos

def pos_splitter_pron_verb(tagged_data, split_weight):
    """
    Adjust weight of word where split is not recommended.

    see: https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points

    Input:
    1D list of Pos objects.
    Split-weight indicating the importance of not-splitting on the word.

    Output: 1D list with Pos object with adjusted weights.
    """
    for index, word in enumerate(tagged_data[:-1]):
        next_word = tagged_data[index+1]

        if word.tag == 'PRON' and next_word.tag == 'VERB':
            word.weight = word.weight - split_weight



def pos_splitter_det_noun(tagged_data, split_weight):
    for index, word in enumerate(tagged_data[:-1]):
        next_word = tagged_data[index+1]

        # Determiner and Noun
        if word.tag == 'DET' and next_word.tag == 'NOUN':
            word.weight = word.weight - split_weight

    return tagged_data


def pos_splitter_prep_phrase(tagged_data, split_weight):
    for index, word in enumerate(tagged_data[:-1]):
        next_word = tagged_data[index+1]
        nextnext = tagged_data[index+2]
        nextnextnext = tagged_data[index+3]

    	# Preposition and phrase
        if word.tag == 'ADP' and ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next_word.tag == 'DET' and nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
            word.weight = 0.4

    return tagged_data

def pos_splitter_conj_phrase(tagged_data, split_weight):
    for index, word in enumerate(tagged_data[:-1]):
        next_word = tagged_data[index+1]
        nextnext = tagged_data[index+2]
        nextnextnext = tagged_data[index+3]

        # Conjuction and phrase
        if word.tag == 'CONJ' and ((next_word.tag == 'DET' and nextnext.tag == 'NOUN') or (next_word.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next_word.tag == 'DET' and nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or (next_word.tag == 'PRON' and nextnext.tag == 'NOUN')):
			word.weight = 0.3

    return tagged_data


def pos_splitter(tagged_data):
    """

    Merges word groups that cannot be split to one Word.
        tag them with str 'No split'

    Input: 1D list of Words.

    Output: 1D list with words merged that cannot be split.
    """

    for index, word in enumerate(tagged_data):

        next = tagged_data[index+1]
        nextnext = tagged_data[index+2]
        nextnextnext = tagged_data[index+3]

		# Determiner plus noun
        if word.tag == 'DT' and next.tag == 'NN':

            tagged_data[index].tag = 'No split'
            tagged_data[index].text = word.text + " " + next.text
            tagged_data[index].end = next.end

            tagged_data.remove(next)

		# Preposition and phrase
        if word.tag == 'ADP' and ((next.tag == 'DET' and nextnext.tag == 'NOUN') or (next.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next.tag == 'DET' and nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or (next.tag == 'PRON' and nextnext.tag == 'NOUN')):
            word.weight = 0.4

		# Conjuction and phrase
        if word.tag == 'CONJ' and ((next.tag == 'DET' and nextnext.tag == 'NOUN') or (next.tag == 'ADJ' and nextnext.tag == 'NOUN') or (next.tag == 'DET' and nextnext.tag == 'ADJ' and nextnextnext.tag == 'NOUN') or (next.tag == 'PRON' and nextnext.tag == 'NOUN')):
			word.weight = 0.3



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
