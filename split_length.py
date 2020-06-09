"""
Splits the captiongroup according to the 42 character limit.
You can change sen to a captiongroup from the data.
"""


def check(data):
    """
    Checks if the current data is equal or less than 42 characters.
    """
    return sum([len(x) for x in data]) <= 42


def split_length(data, number=42, splits=[]):
    """
    Splits the data accordingly and finds the first space and makes the cut
    there. It does the same thing recursivly for words that are left in the
    sentence.
    """
    if check(data):
        splits.append(data)
        return splits

    sentence = " ".join(data)
    while sentence[number] != ' ':
        number -= 1

    splits.append(sentence[:number].split())
    split_length(sentence[number:].split(), splits=splits)
    return splits


if __name__ == '__main__':
    sen = "dit is een hele lange zin met echt wel meerdere characters".split()
    split_length(sen)
