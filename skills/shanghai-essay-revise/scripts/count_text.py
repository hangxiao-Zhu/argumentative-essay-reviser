"""Count a supplied essay body without guessing where headings end."""
import argparse
import json
from pathlib import Path
import sys


def counts(text):
    def is_han(c):
        n = ord(c)
        return (0x3400 <= n <= 0x4DBF or 0x4E00 <= n <= 0x9FFF
                or 0xF900 <= n <= 0xFAFF or 0x20000 <= n <= 0x2FA1F
                or 0x30000 <= n <= 0x323AF)
    han = sum(is_han(c) for c in text)
    return {'han_count': han, 'nonspace_count': sum(not c.isspace() for c in text),
            'within_default_target': 850 <= han <= 950}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count essay BODY only, excluding title and feedback')
    parser.add_argument('--file', type=Path)
    args = parser.parse_args()
    body = args.file.read_text(encoding='utf-8-sig') if args.file else sys.stdin.read()
    print(json.dumps(counts(body), ensure_ascii=False))
