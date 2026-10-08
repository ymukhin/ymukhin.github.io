#!/usr/bin/env python3
"""Create a path-only address SVG without storing the address in the repository.

Requires Inkscape on PATH. The address is prompted without echo and processed
in a temporary directory. Only a metadata-free, outlined SVG is retained.
"""
from __future__ import annotations

import argparse
import getpass
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def render(address: str, output: Path, width: float = 160,
           height: float = 20, font_size: float = 14.6666667) -> None:
    """Outline a single line of text, discarding textual and editor metadata."""
    if not address.strip() or any(c in address for c in '\r\n'):
        raise ValueError('Enter one nonempty line.')
    if min(width, height, font_size) <= 0:
        raise ValueError('Dimensions and font size must be positive.')
    executable = shutil.which('inkscape')
    if not executable:
        raise RuntimeError('Install Inkscape and make its command available on PATH.')
    with tempfile.TemporaryDirectory(prefix='contact-art-') as directory:
        source = Path(directory) / 'input.svg'
        target = Path(directory) / 'outlined.svg'
        source.write_text(
            f'<svg xmlns="{NS}" width="{width:g}" height="{height:g}" '
            f'viewBox="0 0 {width:g} {height:g}">'
            f'<text x="0" y="{height - 5:g}" font-family="Arial, sans-serif" '
            f'font-size="{font_size}" font-weight="400" fill="#000">'
            f'{escape(address)}</text></svg>', encoding='utf-8')
        os.chmod(source, 0o600)
        result = subprocess.run(
            [executable, str(source), '--export-text-to-path', '--export-plain-svg',
             '--export-filename=' + str(target)],
            capture_output=True, text=True, timeout=60, check=False)
        if result.returncode or not target.is_file():
            # Do not echo exporter output: it might contain the user's input.
            raise RuntimeError('Inkscape could not produce the outlined graphic.')
        tree = ET.parse(target).getroot()
        if tree.find('.//{*}text') is not None:
            raise RuntimeError('The export still contains text; output was not saved.')
        paths = tree.findall('{*}path')
        if not paths:
            raise RuntimeError('Expected directly outlined paths; output was not saved.')
        clean = ET.Element(f'{{{NS}}}svg', {
            'width': f'{width:g}', 'height': f'{height:g}',
            'viewBox': f'0 0 {width:g} {height:g}', 'fill': '#000'})
        for path in paths:
            # Never retain aria-label, id, style, title, or editor metadata.
            attributes = {key: path.attrib[key] for key in ('d', 'transform')
                          if key in path.attrib}
            ET.SubElement(clean, f'{{{NS}}}path', attributes)
        encoded = ET.tostring(clean, encoding='unicode') + '\n'
        if address.casefold() in encoded.casefold():
            raise RuntimeError('Text was detected in the output; file was not saved.')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'assets/email.svg')
    parser.add_argument('--width', type=float, default=160)
    parser.add_argument('--height', type=float, default=20)
    parser.add_argument('--font-size', type=float, default=14.6666667)
    args = parser.parse_args()
    try:
        address = getpass.getpass('Address to render (input hidden): ')
        render(address, args.output, args.width, args.height, args.font_size)
    except (ValueError, RuntimeError, subprocess.TimeoutExpired, ET.ParseError) as error:
        raise SystemExit(str(error)) from error
    print(f'Saved path-only SVG: {args.output}')
    print('Preview the image to check that the chosen dimensions fit the complete line.')


if __name__ == '__main__':
    main()
