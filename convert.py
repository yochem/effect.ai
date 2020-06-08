"""
This is where the magic happens.
"""
import caption
import asr


[                           # hele caption
    [                       # een caption group
        Word(),             # een woord
        Word(),
        ...
    ],
    [Word(), Word(), ...]
]


