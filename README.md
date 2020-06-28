# cap - AI powered subtitling

This project converts a JSON speech-to-text file to a fully functional SRT
subtitle file. This SRT file consists of caption groups with if needed, line
breaks according to the [subtitle guidelines of the
BBC](https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points).


## Table of Contents

- [Features](#features)
- [Badges](#badges)
- [Preview](#preview)
- [Installation](#installation)
- [How to run](#how_to_run)
- [Overview functionality](#overview_functionality)
- [Support](#support)


## Features

This project mainly generates proper formatted caption groups given a
transcript with word-timing. It implements the following rules from the BBC
guide mentioned above:

- Part-of-Speech tags
- Punctuation
- Gaps in speech
- Character limit (< 84)
- Line limit (< 42)
- And more to come!


## Badges

![Issues](https://img.shields.io/github/issues-raw/yochem/effect.ai?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/yochem/effect.ai?style=for-the-badge)
![Licence](https://img.shields.io/github/license/yochem/effect.ai?style=for-the-badge)


## Preview

## Installation
1. [Clone](https://bit.ly/2BcAdRs) this repository.
2. Install the package:

```shell
$ pip3 install -e cap
```


## How to use

In your shell, run the following:

```shell
$ cap <asr-file> --output <srt-file>
```

For more options, run `$ cap -h`.

Or use this module in Python:

```python
>>> import cap
>>> subs = cap.group('asr/sample01.asrOutput.json', 'srt-file.srt')
>>> # let's see the return value:
>>> print(*subs[0][:5], sep='\n')
Word(text='thanks', start=0.24, end=0.51, weight=5)
Word(text='to', start=0.51, end=0.6, weight=5)
Word(text='last', start=0.6, end=0.86, weight=5)
Word(text='past', start=0.86, end=1.13, weight=5.64)
Word(text='for\n', start=1.13, end=1.2, weight=5.96)
>>>
>>> # and let's see the content of the written file:
>>> with open('srt-file.srt', 'r') as f:
>>>     for line in f.read().splitlines():
>>>         if not line:
>>>             break
>>>         print(line)
1
00:00:00,240 --> 00:00:02,750
thanks to last past for
sponsoring a portion of this video.
```


## Development

Documentation can be found at [Github Pages](yochem.github.io/caps/).

To install the needed packages for development, run this:

```shell
$ pip3 install -e cap[dev]
```

Also make sure [editorconfig](editorconfig.org/) is installed in your editor
of choice.

When pushing code, first run `$ make check` to lint your code and `$ make doc`
to create the docs.


## Support

Found a bug? Got a question? Please report it using Github
[issues](https://github.com/yochem/effect.ai/issues)!
