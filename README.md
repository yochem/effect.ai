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
2. Install requirements (GNU Make is needed)

```shell
$ make install
```


## How to use

In your shell, run the following:

```shell
$ cap <asr-file> --output <srt-file>
```

For more options, run `$ cap -h`.

Or use this module in Python:

```python
import cap

subs = cap.group('asr-file.json')

with open('srt-file.srt', 'w') as f:
    f.write(subs)
```


## Development

To install the needed packages for development, run this:

```shell
$ make development
```

Also make sure [editorconfig](editorconfig.org/) is installed in your editor
of choice.

When pushing code, first run `$ make check` to lint your code and `# make doc`
to create the docs.


## Support

Found a bug? Got a question? Please report it using Github
[issues](https://github.com/yochem/effect.ai/issues)!
