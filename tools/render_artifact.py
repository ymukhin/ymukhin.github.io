#!/usr/bin/env python3
"""Compile the editable TikZ drawing to the outlined SVG used by the website.

Website deployment does NOT run this script: commit the generated assets.
Local prerequisites: LuaLaTeX, Metropolis, Fira Sans, TikZ, preview, and
Poppler's pdftocairo. Python uses only its standard library.
"""
from __future__ import annotations
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION = (
    'Observed illness–death paths with a probability cloud and censoring cuts. '
    'Blue: recurrence at 3, observed death at 6, censoring at 8. '
    'Orange: censoring at 4 and hidden death at 7.5. '
    'Purple: recurrence at 2, censoring at 5, hidden death at 9. '
    'Pale dashed portions are illustrative unobserved continuations, not estimates.'
)


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=120, check=False)
    if result.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(command)
                           + '\n' + result.stdout[-7000:])
    return result.stdout


def main() -> int:
    for executable in ('lualatex', 'pdftocairo'):
        if not shutil.which(executable):
            print(f'Missing {executable}. Install TeX/Poppler locally, or keep the supplied assets.', file=sys.stderr)
            return 1
    source = ROOT / 'sources/observed-trajectories-web.tex'
    try:
        with tempfile.TemporaryDirectory(prefix='mukhin-trajectory-') as tmp:
            tmp = Path(tmp)
            output = run(['lualatex', '-no-shell-escape', '-interaction=nonstopmode',
                          '-halt-on-error', f'-output-directory={tmp}', str(source)], tmp)
            if 'Could not find Fira Sans fonts' in output:
                raise RuntimeError('Metropolis could not find Fira Sans. Install Fira Sans before rebuilding so the labels retain the intended slide typeface.')
            pdf = tmp / (source.stem + '.pdf')
            svg = tmp / 'drawing.svg'
            run(['pdftocairo', '-svg', str(pdf), str(svg)], tmp)
            text = svg.read_text(encoding='utf-8')
            text = text.replace('<defs>', '<title id="trajectory-title">Stopped trajectories</title>\n'
                                f'<desc id="trajectory-description">{DESCRIPTION}</desc>\n<defs>', 1)
            text = re.sub(r'(<svg\b[^>]*)(>)',
                          r'\1 role="img" aria-labelledby="trajectory-title trajectory-description"\2', text, count=1)
            (ROOT / 'assets/stopped-trajectories.svg').write_text(text, encoding='utf-8')
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print('Updated assets/stopped-trajectories.svg')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
