"""Create a new local Markdown review; never overwrite previous revisions."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re


def safe_title(title):
    title = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', title).strip(' .')[:60]
    return title or '未命名作文'


def save_review(directory, title, content, now=None):
    directory = Path(directory).resolve()
    # The destination must already exist: do not accidentally create a misspelled vault.
    if not directory.is_dir():
        raise FileNotFoundError('Configured output directory does not exist')
    now = now or datetime.now().astimezone()
    stem = f'{now:%Y-%m-%d_%H%M%S}-{safe_title(title)}'
    for i in range(1, 1001):
        path = directory / f'{stem}{"" if i == 1 else "-" + str(i)}.md'
        try:
            with path.open('x', encoding='utf-8', newline='\n') as output:
                output.write(f'<!-- generated_at: {now.isoformat()} -->\n\n{content}')
            return path
        except FileExistsError:
            continue
    raise FileExistsError('Too many reviews with the same timestamp and title')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--title', required=True)
    parser.add_argument('--input', required=True, type=Path)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text(encoding='utf-8-sig'))
    target = Path(profile['output_dir'])
    if not target.is_absolute():
        raise ValueError('output_dir must be an absolute local path')
    content = args.input.read_text(encoding='utf-8-sig')
    if not content.strip():
        raise ValueError('Review is empty')
    print(save_review(target, args.title, content))
