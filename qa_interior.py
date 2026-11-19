#!/usr/bin/env python3
"""Production checks for the KDP interior and the markdown source."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "Bio-Harmonization-KDP-interior.pdf"
SOURCE = ROOT / "manuscript"

FORBIDDEN_PDF = [
    "Proof", "Global Women's Bureau", "89%", "78%", "4.2x",
    "67% achieved", "2998", "\u2014", "\u2013", "\u201c", "\u201d",
]
FORBIDDEN_SOURCE = [
    "\u2014", "\u2013", "\u201c", "\u201d",
    "not just", "not merely", "Let's dive", "Here's what you need to know",
    "I hope this helps", "showcase", "tapestry", "pivotal", "delve",
]


def main() -> int:
    failures: list[str] = []
    if not PDF.exists():
        print(f"FAIL: {PDF.name} is missing")
        return 1

    reader = PdfReader(str(PDF))
    texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(texts)

    sizes = {(round(float(p.mediabox.width), 1), round(float(p.mediabox.height), 1))
             for p in reader.pages}
    if sizes != {(432.0, 648.0)}:
        failures.append(f"unexpected page sizes: {sizes}")

    for token in FORBIDDEN_PDF:
        if token in all_text:
            failures.append(f"forbidden text in PDF: {token!r}")

    fonts = set()
    for page in reader.pages:
        for font in ((page.get("/Resources") or {}).get("/Font") or {}).values():
            fonts.add(str(font.get_object().get("/BaseFont")))
    non_embedded = sorted(f for f in fonts if "+" not in f)
    if non_embedded:
        failures.append(f"font resources without embedding prefix: {non_embedded}")

    entries = re.findall(
        r"(Part [IVX]+: [^\n]+|Chapter \d+: [^\n]+|Epilogue: [^\n]+|"
        r"Appendix [A-D]: [^\n]+|References|About the author)\s+(\d+)",
        "\n".join(texts[7:9]),
    )
    for title, page_no in entries:
        index = int(page_no) - 1
        if index >= len(texts) or title not in texts[index].replace("\n", " "):
            failures.append(f"contents mismatch: {title!r} -> page {page_no}")

    for path in SOURCE.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_SOURCE:
            if token.lower() in text.lower():
                failures.append(f"{path.name}: review pattern {token!r}")

    print(f"Pages: {len(reader.pages)}; words: {len(all_text.split())}")
    print(f"Embedded font subsets: {sorted(fonts)}")
    print(f"Contents entries checked: {len(entries)}")
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" -", failure)
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
