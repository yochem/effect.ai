# effect.ai - AI powered subtitling
> This project converts a JSON speech-to-text file to a fully functional SRT
subtitle file. This SRT file consists of caption groups with if needed, line
breaks according to the subtitle guidelines of the BBC.

> https://bbc.github.io/subtitle-guidelines/#Break-at-natural-points


---

## Table of Contents (Optional)

> If your `README` has a lot of info, section headers might be nice.

- [Badges](#badges)
- [Preview](#preview)
- [Installation](#installation)
- [Overview functionality](#overview_functionality)
- [Support](#support)

---

### Badges
![Issues](https://img.shields.io/bitbucket/issues-raw/yochem/effect.ai?style=for-the-badge)     ![Last Commit](https://img.shields.io/github/last-commit/yochem/effect.ai?style=for-the-badge)  ![Licence](https://img.shields.io/github/license/yochem/effect.ai?style=for-the-badge)

---

### Preview
<INSERT VIDEO WITH SUBTITLES>

---

### Installation
#### Clone
- Clone this repo to your local machine using 'git@github.com:yochem/effect.ai.git'

#### Setup
Update and install the following packages:
> SRT
```shell
$ pip3 install srt
```

> NLTK
```shell
$ pip3 install nltk
```

---

### Overview functionality

```
.
├── asr.py
│   ├── Word(): Word with start time, end time and weight
│   ├── Punc(): Punctuation with start and end time being end time of prev word plus weight
│   └── ASR(): Class for loading in an ASR file
│       ├── transcript(): Return the transcript as one big string.
│       ├── json(): Return the full JSON file as python dictionary.
│       └── groups(): Convert the ASR to the following format
├── caption.py
|   ├── create_subtitles(): Creates a start time and end time for each caption group
│   ├── compose(): Compose a SRT string from captions
│   └── write(): Compose SRT string and write to file
├── convert.py
│   ├── basic_error(): Compares generated subs with manual subs
|   ├── split_weights(): Creates caption groups by splitting the highest weight
|   └── create_groups(): Adds weights and lists order of importance of POS
├── weighting.py
|   ├── Pos(): Word with start time, end time, weight and POS-tag
|   ├── pos_tag(): Adds POS-tag
|   ├── pos_pron_verb(): Lowers weight between pronoun+verb
|   ├── pos_det_noun(): Lowers weight between determiner+noun  
|   ├── pos_prep_phrase(): Lowers weight between prepostion+following phrase
|   ├── pos_conj_phrase(): Lowers weight between conjunction+following phrase
|   ├── speech_gaps(): Adds weight to word before speech gaps
|   ├── punctuation(): Adds weight to punctuation
|   ├── length(): Returns list of possible splits
|   └── split_length(): Adds weights according to length()
```

---

## Support

Reach out to us at one of the following places!
<ff mailtj>

-
