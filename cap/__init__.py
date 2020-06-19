"""
.. include:: ../README.md
"""


from . import asr
from . import caption
from . import convert
from . import weighting


def group(asr_file: str) -> str:
    """Convert ASR to SRT file with well formatted caption groups.

    Args:
        asr_file: Filename of the ASR file.

    Returns:
        The content of a srt file as string, which can be written to a srt
        file.
    """
    data = asr.ASR(asr_file).groups()
    groups = convert.create_groups(data)
    return caption.compose(groups)
