def check(data):
    """Checks if the current data is equal or less than 42 characters."""
    return sum([len(x) for x in data]) <= 42


def length(data, number=42, splits=[]):
    """
    Splits the data accordingly and finds the first space and makes the cut
    there. It does the same thing recursivly for words that are left in the
    sentence.
    """
    if check(data):
        splits.append(data)
        return splits

    sentence = ' '.join(data)
    while sentence[number] != ' ':
        number -= 1

    splits.append(sentence[:number].split())
    length(sentence[number:].split(), splits=splits)
    return splits


def split_length(data):
    """
    Takes the datastructure as input and outputs the same datastructure with
    the changed weights according to a 42 character limit.
    """
    sentence = [word.text for word in data]
    splits = length(sentence)

    number = 0
    for split in splits:
        number += len(split)
        data[number-1].weight += 1
        data[number-2].weight += 0.5
        data[number-3].weight += 0.25

    return data
