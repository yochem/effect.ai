import json
from typing import List
import sys
from datetime import timedelta
import srt


def write_srt(subs: List[srt.Subtitle], filename=sys.stdout) -> None:
    composed = srt.compose(subs)

    if filename == sys.stdout:
        print(composed)
        return

    with open(filename, 'w') as f:
        f.write(composed)


def load_asr(filename: str) -> dict:
    """Load asr file with given filename. Returns JSON object as dict."""
    with open(filename, 'r') as f:
        raw = f.read()

    return json.loads(raw)


def process(word_objects) -> List[srt.Subtitle]:
    subs = []
    subtitle = dict()
    index = 1

    for word in word_objects:
        if 'start' not in subtitle:
            subtitle['start'] = word['start_time']
            subtitle['content'] = []

        if 'end_time' in word:
            subtitle['end'] = word['end_time']

        content = word['alternatives'][0]['content']
        if word['type'] == 'pronunciation':
            subtitle['content'].append(content)

        if word['type'] == 'punctuation':
            subtitle_content = ' '.join(subtitle['content']) + content
            subs.append(srt.Subtitle(index,
                                     timedelta(seconds=float(subtitle['start'])),
                                     timedelta(seconds=float(subtitle['end'])),
                                     subtitle_content))
            index += 1
            subtitle = dict()

    return subs


if __name__ == '__main__':
    data = load_asr('asr/sample01.asrOutput.json')
    words = data['results']['items']
    subtitles = process(words)
    write_srt(subtitles, filename='sample01.srt')
