"""Audit the EXACT staged file set against a reviewed allowlist before commit."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def violations(path, data, allowed):
    problems = []
    if path not in allowed:
        problems.append('not in reviewed allowlist')
    if b'\0' in data:
        problems.append('binary content')
    text = data.decode('utf-8-sig', errors='replace')
    if re.search(r'(?i)(?:[A-Z]:[\\/](?:Users|OneDrive|Project|作文)|sk-[a-zA-Z0-9]{20,}|gh[pousr]_[a-zA-Z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)', text):
        problems.append('local path or credential-like content')
    return problems


def main():
    allow_path = ROOT / 'PUBLIC_FILES.txt'
    allowed = {x for x in allow_path.read_text(encoding='utf-8').splitlines() if x and not x.startswith('#')}
    staged = [x for x in git('ls-files', '-z').decode('utf-8').split('\0') if x]
    errors = []
    # Private originals and extraction must remain ignored, even before staging.
    for private in ['训练数据', '范文资料', '.private', 'PROJECT_STATUS.md']:
        probe = subprocess.run(['git', '-C', str(ROOT), 'check-ignore', '-q', private], capture_output=True)
        if probe.returncode != 0:
            errors.append(f'{private}: not ignored')
    for path in staged:
        data = git('show', ':' + path)
        errors.extend(f'{path}: {why}' for why in violations(path, data, allowed))
    if not staged:
        errors.append('empty index; nothing audited')
    print(f'Audited {len(staged)} staged files; {len(errors)} issues')
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
