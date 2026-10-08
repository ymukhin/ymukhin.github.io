#!/usr/bin/env python3
"""Refresh the inline citation disclosure from publications.bib (standard library).

Run after editing publications.bib. Commit the updated index.html alongside it.
Only the Python standard library is used; the website itself runs no Python.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]


def citation_block(bib: str) -> str:
    return '''        <!-- BEGIN GENERATED CITATIONS -->
        <details class="citation-tools" id="citations">
          <summary>Citations (BibTeX)</summary>
          <p><a href="publications.bib" type="text/plain" download="mukhin-publications.bib">Download .bib file</a></p>
          <pre><code>''' + escape(bib.rstrip()) + '''</code></pre>
        </details>
        <!-- END GENERATED CITATIONS -->'''


def sync() -> None:
    page = ROOT / 'index.html'
    source = page.read_text(encoding='utf-8')
    pattern = r'        <!-- BEGIN GENERATED CITATIONS -->.*?        <!-- END GENERATED CITATIONS -->'
    output, count = re.subn(pattern, lambda _: citation_block((ROOT / 'publications.bib').read_text(encoding='utf-8')), source, flags=re.S)
    if count != 1:
        raise SystemExit(f'Expected one citation block in index.html; found {count}.')
    page.write_text(output, encoding='utf-8')
    print(page)


if __name__ == '__main__':
    sync()
