"""
Splits the captiongroup according to the 42 character limit.
def check checks if the current data is equal or less than 42 characters
def splitlength splits the data accordingly and finds the first space adn makes
the cut there.
It does recursivly the same thing for words that are left in the sentence.

You can change sen to a captiongroup from the data
"""


def check(data):
    return sum([len(x) for x in data]) <= 42


def splitlength(data, number=42, splits=[]):
    if check(data):
        splits.append(data)
        return splits

    sentence = " ".join(data)
    while sentence[number] != " ":
        number -= 1

    splits.append(sentence[:number].split())
    splitlength(sentence[number:].split(), splits=splits)
    return splits


if __name__ == '__main__':
    sen = "dit is een hele lange zin met echt wel meerdere characters".split()
    splitlength(sen)
