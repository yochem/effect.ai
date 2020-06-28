"""
.. include:: ../README.md
"""
from . import asr
from . import caption
from . import convert
from . import weighting


def group(asr_file: str, srt_file: str = None) -> convert.Groups:
    """Convert ASR to SRT file with well formatted caption groups.

    This function is the main interface for the module. Given a filename of an
    ASR file, this function parses the subtitles, groups them and if given an
    output filename, writes them to a file.

    Args:
        asr_file: Filename of the ASR file.
        srt_file: Filename to which the SRT output will be written.

    Returns:
        The caption groups, consists of a list of our custom Caption-list
        dataformats.
    """
    data = asr.ASR(asr_file).groups()
    groups = convert.create_groups(data)

    if srt_file:
        caption.write(groups, srt_file)

    return groups
