# effect.ai - AI powered subtitling

Overview functionality:

```
.
├── asr.py
│   ├── Word(): word with start time and end time
│   ├── Punc(): punctuation with start and end time being end time of prev word
│   └── ASR(): class for loading in an ASR file
│       ├── transcript(): Return the transcript as one big string.
│       ├── json(): Return the full JSON file as python dictionary.
│       └── groups(): Convert the ASR to the following format
├── caption.py
│   ├── compose(): Compose a SRT string from captions
│   └── write(): Compose SRT string and write to file
└── convert.py
```
