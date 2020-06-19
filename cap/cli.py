"""The command line interface for this module.

This file contains functions which are used by the command line interface. It
is used by the 'special' file __main__.py.
"""
import argparse
import json
import os
import sys
import traceback
from typing import Any

from . import asr, convert, caption


def err_print(*args: Any, **kwargs: Any) -> None:
    """Print to stderr."""
    print('ERROR:', *args, file=sys.stderr, **kwargs)
    sys.exit(1)


def cli(args: argparse.Namespace) -> None:
    """The command line interface for cap.

    This function first parses the provided ASR data using
    the ASR class from the asr module. It then creates caption groups using
    create_groups() from the convert module. After that, it's converted to a
    SRT file using the write() function from the caption module.

    Args:
        args: All command line arguments. Run cap -h to see options.
    """
    try:
        data = asr.ASR(args.file).groups()
    except FileNotFoundError:
        err_print(f'{args.file}: No such file')
    except (json.decoder.JSONDecodeError, KeyError, TypeError):
        if args.verbose:
            err_print(traceback.format_exc())
        else:
            err_print('Something went wrong with parsing the ASR file, run',
                      'with the --verbose option to see the error')

    groups = convert.create_groups(data)

    # default name: sample.json -> sample.srt
    name, _ = os.path.splitext(args.file)
    out_file = args.output or name + '.srt'

    caption.write(groups, out_file)
