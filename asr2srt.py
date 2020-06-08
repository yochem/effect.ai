from typing import List
from datetime import timedelta

import srt

import caption
from asr import ASR



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
            start_time = timedelta(seconds=float(subtitle['start']))
            end_time = timedelta(seconds=float(subtitle['end']))

            subs.append(srt.Subtitle(index, start_time, end_time,
                                     subtitle_content))
            index += 1
            subtitle = dict()

    return subs


if __name__ == '__main__':
    data = ASR('asr/sample01.asrOutput.json').json()
    words = data['results']['items']
    subtitles = process(words)
    caption.write(subtitles, filename='sample01.srt')
