#!/usr/bin/env python3
"""Download and unpack the pinned Ghostscript runtime used to build the report."""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / '.tools/ghostscript-9.55.0'


def environment():
    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = str(TOOL / 'usr/lib/x86_64-linux-gnu')
    env['GS_LIB'] = ':'.join(str(TOOL / 'usr/share/ghostscript/9.55.0' / p)
                             for p in ('Resource/Init', 'lib'))
    return env


def main():
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise SystemExit('This archived toolchain requires Linux x86_64.')
    TOOL.mkdir(parents=True, exist_ok=True)
    packages = json.loads((ROOT / 'scripts/ghostscript-packages.json').read_text())
    for package in packages:
        destination = TOOL / package['name']
        if not destination.exists():
            print('Downloading', package['name'], flush=True)
            temporary = destination.with_suffix('.download')
            urllib.request.urlretrieve(package['url'], temporary)
            if hashlib.sha256(temporary.read_bytes()).hexdigest() != package['sha256']:
                raise SystemExit(f'Checksum mismatch: {temporary}')
            temporary.rename(destination)
        if hashlib.sha256(destination.read_bytes()).hexdigest() != package['sha256']:
            raise SystemExit(f'Checksum mismatch: {destination}')
        subprocess.run(['dpkg-deb', '-x', str(destination), str(TOOL)], check=True)
    subprocess.run([str(TOOL / 'usr/bin/gs'), '--version'], env=environment(), check=True)


if __name__ == '__main__':
    main()
