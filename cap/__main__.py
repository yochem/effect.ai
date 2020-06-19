import argparse

from .cli import cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Name of the srt file')
    parser.add_argument('file', help='The ASR file to extract data from')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show traceback if error occurs')

    cli(parser.parse_args())
