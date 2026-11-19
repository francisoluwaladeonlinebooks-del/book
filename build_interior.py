#!/usr/bin/env python3
"""Build a single-page KDP print interior from the revised markdown manuscript.

Trim: 6 x 9 in. Single pages, embedded TTF fonts, running heads, page numbers.
No crop marks, no registration marks, no placeholder or proofing text.
"""

from __future__ import annotations

import re
from pathlib import Path

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript"
OUTPUT = ROOT / "Bio-Harmonization-KDP-interior.pdf"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

FILES = [
    "00-title.md",
    "01-copyright.md",
    "02-dedication.md",
    "03-medical-disclaimer.md",
    "04-how-to-read-this-book.md",
    "05-authors-note.md",
    "06-contents.md",
    "10-part-i.md",
    "11-chapter-01.md",
    "12-chapter-02.md",
    "13-chapter-03.md",
    "20-part-ii.md",
    "21-chapter-04.md",
    "22-chapter-05.md",
    "23-chapter-06.md",
    "30-part-iii.md",
    "31-chapter-07.md",
    "32-chapter-08.md",
    "33-chapter-09.md",
    "34-chapter-10.md",
    "35-chapter-11.md",
    "40-part-iv.md",
    "41-chapter-12.md",
    "42-chapter-13.md",
    "43-chapter-14.md",
    "50-part-v.md",
    "51-chapter-15.md",
    "52-chapter-16.md",
    "60-epilogue.md",
    "70-appendix-a.md",
    "71-appendix-b.md",
    "72-appendix-c.md",
    "73-appendix-d.md",
    "80-references.md",
    "90-about-the-author.md",
]

PAGE_W, PAGE_H = 6 * inch, 9 * inch
LEFT, RIGHT, TOP, BOTTOM = 0.88 * inch, 0.68 * inch, 0.86 * inch, 0.78 * inch
BODY_W = PAGE_W - LEFT - RIGHT


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("BodySerif", str(FONT_DIR / "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("HeadSans", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("PlainSans", str(FONT_DIR / "DejaVuSans.ttf")))
    rl_config.canvas_basefontname = "PlainSans"


def make_styles():
    return {
        "chapter": ParagraphStyle(
            "chapter", fontName="HeadSans", fontSize=17, leading=22,
            textColor=colors.HexColor("#1a2733"), spaceBefore=0, spaceAfter=22,
            keepWithNext=True, alignment=TA_LEFT,
        ),
        "part": ParagraphStyle(
            "part", fontName="HeadSans", fontSize=21, leading=28,
            textColor=colors.HexColor("#1a2733"), alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "part_sub": ParagraphStyle(
            "part_sub", fontName="PlainSans", fontSize=11, leading=17,
            textColor=colors.HexColor("#4a5a68"), alignment=TA_CENTER,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="HeadSans", fontSize=11.4, leading=16,
            textColor=colors.HexColor("#263a4a"), spaceBefore=16, spaceAfter=7,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="HeadSans", fontSize=10, leading=14,
            spaceBefore=11, spaceAfter=5, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", fontName="BodySerif", fontSize=10.1, leading=15.1,
            alignment=TA_JUSTIFY, spaceAfter=8, allowWidows=0, allowOrphans=0,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="BodySerif", fontSize=10.1, leading=14.6,
            alignment=TA_LEFT, leftIndent=16, bulletIndent=3, spaceAfter=5,
            allowWidows=0, allowOrphans=0,
        ),
        "number": ParagraphStyle(
            "number", fontName="BodySerif", fontSize=10.1, leading=14.6,
            alignment=TA_LEFT, leftIndent=18, bulletIndent=3, spaceAfter=5,
            allowWidows=0, allowOrphans=0,
        ),
        "title": ParagraphStyle(
            "title", fontName="HeadSans", fontSize=25, leading=33,
            alignment=TA_CENTER, textColor=colors.HexColor("#1a2733"),
        ),
        "title_sub": ParagraphStyle(
            "title_sub", fontName="PlainSans", fontSize=15, leading=24,
            alignment=TA_CENTER, spaceBefore=20,
        ),
        "title_author": ParagraphStyle(
            "title_author", fontName="PlainSans", fontSize=11.5, leading=18,
            alignment=TA_CENTER, spaceBefore=110,
        ),
        "small": ParagraphStyle(
            "small", fontName="BodySerif", fontSize=9.4, leading=14,
            alignment=TA_LEFT, spaceAfter=7,
        ),
        "dedication": ParagraphStyle(
            "dedication", fontName="BodySerif", fontSize=10.5, leading=17,
            alignment=TA_LEFT, spaceAfter=10, leftIndent=12,
        ),
        "toc_head": ParagraphStyle(
            "toc_head", fontName="HeadSans", fontSize=16, leading=22,
            spaceAfter=18,
        ),
    }


class SectionHeading(Paragraph):
    """Marker flowable used to collect table-of-contents entries."""


class InteriorDoc(BaseDocTemplate):
    def __init__(self, *args, collector, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector = collector

    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionHeading):
            self.collector.append(
                (flowable.toc_level, flowable.getPlainText(), self.page)
            )


def clean(text: str) -> str:
    text = text.replace("**", "").replace("*", "")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def markdown_to_flowables(name: str, styles: dict, collected: list) -> list:
    raw = (MANUSCRIPT / name).read_text(encoding="utf-8").strip()
    lines = raw.splitlines()
    out: list = []
    buffer: list[str] = []
    part_mode = False

    def flush() -> None:
        if buffer:
            text = " ".join(x.strip() for x in buffer if x.strip())
            if text:
                out.append(Paragraph(clean(text), styles["body"]))
            buffer.clear()

    if name == "00-title.md":
        parts = [x.strip() for x in lines if x.strip()]
        out += [
            Spacer(1, 2.0 * inch),
            Paragraph(clean(parts[0]), styles["title"]),
            Paragraph(clean(parts[1]), styles["title_sub"]),
            Paragraph(clean(parts[2]), styles["title_author"]),
        ]
        return out

    for line in lines:
        stripped = line.strip()
        if stripped == "<!-- part -->":
            part_mode = True
            continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("# "):
            flush()
            title = clean(stripped[2:])
            if part_mode:
                subtitle = ""
                out.append(PageBreak())
                out.append(Spacer(1, 2.5 * inch))
                heading = SectionHeading(title, styles["part"])
                heading.toc_level = 0
                out.append(heading)
                # The following line is the part subtitle, handled in the next pass.
                part_mode = "subtitle"
                continue
            out.append(PageBreak())
            heading = SectionHeading(title, styles["chapter"])
            heading.toc_level = 1
            out.append(heading)
            continue
        if part_mode == "subtitle":
            out.append(Paragraph(clean(stripped), styles["part_sub"]))
            part_mode = False
            continue
        if stripped.startswith("## "):
            flush()
            out.append(Paragraph(clean(stripped[3:]), styles["h2"]))
            continue
        if stripped.startswith("### "):
            flush()
            out.append(Paragraph(clean(stripped[4:]), styles["h3"]))
            continue
        if stripped.startswith("- "):
            flush()
            out.append(Paragraph(clean(stripped[2:]), styles["bullet"], bulletText="\u2022"))
            continue
        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            flush()
            number = stripped.split(".", 1)[0] + "."
            out.append(Paragraph(clean(match.group(1)), styles["number"], bulletText=number))
            continue
        buffer.append(stripped)
    flush()
    return out


def build_toc(entries: list[tuple[int, str, int | None]], styles: dict) -> list:
    flowables: list = [Paragraph("Contents", styles["toc_head"])]
    for level, title, page in entries:
        label = ("\u2002\u2002" if level else "") + clean(title)
        number = str(page) if page else "00"
        row = Table([[label, number]], colWidths=[BODY_W - 36, 36])
        row.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "PlainSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.7),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#263a4a")),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        flowables.append(row)
    return flowables


def make_doc(path: Path, collected_out: list, toc_entries: list | None) -> BaseDocTemplate:
    doc = InteriorDoc(str(path), collector=collected_out, pagesize=(PAGE_W, PAGE_H),
        leftMargin=LEFT, rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM,
        title="Bio-Harmonization: The Bureau Protocol",
        author="Olabode Johnson Ilesanmi",
        subject="A practical framework for organising women's health information",
        creator="Olabode Johnson Ilesanmi",
        pageCompression=1,
    )
    frame = Frame(LEFT, BOTTOM, BODY_W, PAGE_H - TOP - BOTTOM, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def draw_front(canvas, document):
        canvas.saveState()
        canvas.restoreState()

    def draw_body(canvas, document):
        canvas.saveState()
        canvas.setFont("PlainSans", 7.6)
        canvas.setFillColor(colors.HexColor("#6b7781"))
        if document.page % 2 == 0:
            canvas.drawString(LEFT, PAGE_H - 0.56 * inch, "Bio-Harmonization: The Bureau Protocol")
        else:
            canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 0.56 * inch,
                                   "Olabode Johnson Ilesanmi")
        canvas.setFont("PlainSans", 8.4)
        canvas.drawCentredString(PAGE_W / 2, 0.42 * inch, str(document.page))
        canvas.restoreState()

    doc.addPageTemplates([
        PageTemplate(id="front", frames=[frame], onPage=draw_front),
        PageTemplate(id="body", frames=[frame], onPage=draw_body),
    ])

    styles = make_styles()
    collected: list = []
    story: list = []
    for name in FILES:
        if name in {"01-copyright.md", "02-dedication.md", "03-medical-disclaimer.md",
                    "04-how-to-read-this-book.md", "05-authors-note.md"}:
            out = markdown_to_flowables(name, styles, collected)
            story.append(PageBreak())
            story.extend(out)
            continue
        if name == "06-contents.md":
            entries = toc_entries if toc_entries is not None else [
                (level, title, None) for level, title in collected
            ]
            story.append(NextPageTemplate("body"))
            story.extend(build_toc(entries, styles))
            continue
        story.extend(markdown_to_flowables(name, styles, collected))
    doc.build(story)
    return doc


def strip_unused_fonts(path: Path) -> None:
    """Drop the unused Helvetica resource that reportlab adds at page setup."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return
    reader = PdfReader(str(path))
    writer = PdfWriter()
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        fonts = resources.get("/Font")
        if fonts:
            fonts = fonts.get_object()
            stream = page.get_contents().get_data().decode("latin-1")
            for key in list(fonts.keys()):
                font = fonts[key].get_object()
                if str(font.get("/BaseFont")) == "/Helvetica" and str(key) not in stream:
                    del fonts[key]
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Bio-Harmonization: The Bureau Protocol",
        "/Author": "Olabode Johnson Ilesanmi",
        "/Subject": "A practical framework for organising women's health information",
    })
    with path.open("wb") as handle:
        writer.write(handle)


def main() -> None:
    for required in ("00-title.md", "80-references.md"):
        if not (MANUSCRIPT / required).exists():
            raise SystemExit(f"missing manuscript file: {required}")

    register_fonts()

    # Pass 1 has no entries in the contents; later passes feed real page numbers back in.
    entries: list = []
    for attempt in range(1, 6):
        collected: list = []
        make_doc(OUTPUT, collected, entries)
        if collected == entries:
            print(f"TOC page numbers stable after pass {attempt}")
            break
        entries = collected
    else:
        raise SystemExit("TOC page numbers did not stabilise")
    titles = len(entries)

    strip_unused_fonts(OUTPUT)

    size = OUTPUT.stat().st_size
    print(f"Wrote {OUTPUT.name}: {size:,} bytes")
    print(f"Headings in contents: {titles}")


if __name__ == "__main__":
    main()
