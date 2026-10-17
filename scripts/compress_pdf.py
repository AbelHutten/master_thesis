#!/usr/bin/env python3
"""Compress the compiled report using its original Ghostscript settings."""

import subprocess

from setup_ghostscript import ROOT, TOOL, environment


def main():
    gs = TOOL / 'usr/bin/gs'
    if not gs.exists():
        raise SystemExit('Run make tools to obtain Ghostscript 9.55.0.')
    env = environment()
    # The archived PDF records 2023-05-01 22:49:33 +02:00.
    env['SOURCE_DATE_EPOCH'] = '1682974173'
    command = [
        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/printer', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        '-sOutputFile=build/thesis.pdf', 'build/Report.pdf',
    ]
    subprocess.run(command, executable=str(gs), cwd=ROOT, env=env, check=True)


if __name__ == '__main__':
    main()
