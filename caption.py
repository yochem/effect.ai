import sys
from typing import List

import srt


def write(subs: List[srt.Subtitle], filename=sys.stdout) -> None:
    composed = srt.compose(subs)

    if filename == sys.stdout:
        print(composed)
        return

    with open(filename, 'w') as f:
        f.write(composed)
