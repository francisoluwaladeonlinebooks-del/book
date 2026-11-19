#!/usr/bin/env python3
"""Build one reviewer/editor PDF from the manuscript and editorial material."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

import build_interior as book

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Bio-Harmonization-Review-Package.pdf"

REVIEW_FILES = [
    ROOT / "review" / "00-review-cover.md",
    ROOT / "review" / "01-review-brief.md",
]

MANUSCRIPT_FILES = [
    "00-title.md", "01-copyright.md", "02-dedication.md", "03-medical-disclaimer.md",
    "04-how-to-read-this-book.md", "05-authors-note.md", "10-part-i.md",
    "11-chapter-01.md", "12-chapter-02.md", "13-chapter-03.md",
    "20-part-ii.md", "21-chapter-04.md", "22-chapter-05.md", "23-chapter-06.md",
    "30-part-iii.md", "31-chapter-07.md", "32-chapter-08.md", "33-chapter-09.md",
    "34-chapter-10.md", "35-chapter-11.md", "40-part-iv.md", "41-chapter-12.md",
    "42-chapter-13.md", "43-chapter-14.md", "50-part-v.md", "51-chapter-15.md",
    "52-chapter-16.md", "60-epilogue.md", "70-appendix-a.md", "71-appendix-b.md",
    "72-appendix-c.md", "73-appendix-d.md", "80-references.md",
    "90-about-the-author.md",
]

EDITORIAL_FILES = [
    ROOT / "editorial" / "evidence-audit.md",
    ROOT / "editorial" / "editorial-report.md",
    ROOT / "editorial" / "clinical-review-packet.md",
    ROOT / "editorial" / "kdp-submission-checklist.md",
    ROOT / "review" / "02-query-log.md",
]

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.92 * 100
TOP, BOTTOM = 0.85 * 100, 0.8 * 100
BODY_W = PAGE_W - LEFT - RIGHT


def make_styles() -> dict:
    return {
        "chapter": ParagraphStyle("r_chapter", fontName="HeadSans", fontSize=16,
                                  leading=21, spaceBefore=0, spaceAfter=16,
                                  textColor=colors.HexColor("#1a2733")),
        "part": ParagraphStyle("r_part", fontName="HeadSans", fontSize=20,
                               leading=27, alignment=TA_CENTER, spaceAfter=14,
                               textColor=colors.HexColor("#1a2733")),
        "part_sub": ParagraphStyle("r_part_sub", fontName="PlainSans", fontSize=11,
                                   leading=17, alignment=TA_CENTER,
                                   textColor=colors.HexColor("#4a5a68")),
        "h2": ParagraphStyle("r_h2", fontName="HeadSans", fontSize=11.6,
                             leading=16, spaceBefore=14, spaceAfter=6,
                             textColor=colors.HexColor("#263a4a")),
        "h3": ParagraphStyle("r_h3", fontName="HeadSans", fontSize=10.3,
                             leading=14, spaceBefore=10, spaceAfter=5),
        "body": ParagraphStyle("r_body", fontName="BodySerif", fontSize=10.6,
                               leading=16, spaceAfter=8, allowWidows=0,
                               allowOrphans=0),
        "bullet": ParagraphStyle("r_bullet", fontName="BodySerif", fontSize=10.4,
                                 leading=15.4, leftIndent=17, bulletIndent=3,
                                 spaceAfter=5, allowWidows=0, allowOrphans=0),
        "number": ParagraphStyle("r_number", fontName="BodySerif", fontSize=10.4,
                                 leading=15.4, leftIndent=19, bulletIndent=3,
                                 spaceAfter=5, allowWidows=0, allowOrphans=0),
        "title": ParagraphStyle("r_title", fontName="HeadSans", fontSize=17,
                                leading=25, textColor=colors.HexColor("#1a2733")),
        "title_sub": ParagraphStyle("r_title_sub", fontName="PlainSans", fontSize=12,
                                    leading=19, spaceBefore=16),
        "title_author": ParagraphStyle("r_title_author", fontName="PlainSans",
                                       fontSize=11, leading=18, spaceBefore=70),
        "small": ParagraphStyle("r_small", fontName="BodySerif", fontSize=10.2,
                                leading=15.5, spaceAfter=8),
        "dedication": ParagraphStyle("r_dedication", fontName="BodySerif",
                                     fontSize=10.8, leading=17, leftIndent=12,
                                     spaceAfter=10),
        "toc_head": ParagraphStyle("r_toc_head", fontName="HeadSans", fontSize=18,
                                   leading=24, spaceAfter=18),
        "table_head": ParagraphStyle("r_th", fontName="HeadSans", fontSize=8.6,
                                     leading=11.4, textColor=colors.white),
        "table_cell": ParagraphStyle("r_tc", fontName="BodySerif", fontSize=8.6,
                                     leading=11.6),
        "review_title": ParagraphStyle("r_review_title", fontName="HeadSans",
                                       fontSize=25, leading=34, alignment=TA_CENTER,
                                       textColor=colors.HexColor("#1a2733")),
        "review_sub": ParagraphStyle("r_review_sub", fontName="PlainSans",
                                     fontSize=13, leading=21, alignment=TA_CENTER,
                                     spaceBefore=26),
        "review_meta": ParagraphStyle("r_review_meta", fontName="PlainSans",
                                      fontSize=11, leading=19, alignment=TA_CENTER,
                                      spaceBefore=70),
        "review_status": ParagraphStyle("r_review_status", fontName="HeadSans",
                                        fontSize=10.5, leading=17,
                                        alignment=TA_CENTER, spaceBefore=34,
                                        textColor=colors.HexColor("#8a4b1e")),
    }


def clean(text: str) -> str:
    text = book.clean(text)
    return text.replace("`", "")


def parse_table(lines: list[str], styles: dict) -> tuple[list, int]:
    rows = []
    index = 0
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        row = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if not all(set(cell) <= set("-: ") for cell in row):
            rows.append(row)
        index += 1
    if not rows:
        return [], index
    width = len(rows[0])
    if rows[0] and rows[0][0] == "#":
        col_widths = [0.05 * BODY_W, 0.31 * BODY_W, 0.31 * BODY_W, 0.33 * BODY_W]
    elif width == 4:
        col_widths = [0.18 * BODY_W, 0.34 * BODY_W, 0.18 * BODY_W, 0.30 * BODY_W]
    elif width == 5:
        col_widths = [0.10 * BODY_W, 0.18 * BODY_W, 0.32 * BODY_W, 0.27 * BODY_W, 0.13 * BODY_W]
    else:
        col_widths = [BODY_W / width] * width

    data = [[Paragraph(clean(cell), styles["table_head"]) for cell in rows[0]]]
    for row in rows[1:]:
        data.append([Paragraph(clean(cell), styles["table_cell"]) for cell in row])
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#263a4a")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#b9c3ca")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f3f5f6")]),
    ]))
    return [Spacer(1, 5), table, Spacer(1, 9)], index


def render_cover(styles: dict) -> list:
    lines = [x.strip() for x in (ROOT / "review" / "00-review-cover.md").read_text().splitlines()
             if x.strip() and not x.startswith("<!--")]
    return [
        Spacer(1, 1.6 * 100),
        Paragraph(clean(lines[0]), styles["review_title"]),
        Paragraph(clean(lines[1]), styles["review_sub"]),
        Paragraph(clean(lines[2]), styles["review_sub"]),
        Paragraph(clean(lines[3]), styles["review_meta"]),
        Paragraph(clean(lines[4]), styles["review_meta"]),
        Paragraph(clean(lines[5]), styles["review_status"]),
    ]


def render_markdown(path: Path, styles: dict) -> tuple[list, list]:
    raw = path.read_text(encoding="utf-8").strip()
    if raw.startswith("<!-- review-cover -->"):
        return render_cover(styles), []
    if path.name == "00-title.md":
        parts = [x.strip() for x in raw.splitlines() if x.strip()]
        return [
            Spacer(1, 2.0 * 100),
            Paragraph(clean(parts[0]), styles["review_title"]),
            Paragraph(clean(parts[1]), styles["review_sub"]),
            Paragraph(clean(parts[2]), styles["review_meta"]),
            PageBreak(),
        ], []
    lines = raw.splitlines()
    flowables: list = []
    headings: list = []
    buffer: list[str] = []
    part_mode = False
    is_book = path.parent == book.MANUSCRIPT and path.name in book.FILES

    def flush() -> None:
        if buffer:
            text = " ".join(x.strip() for x in buffer if x.strip())
            if text:
                flowables.append(Paragraph(clean(text), styles["body"]))
            buffer.clear()

    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped == "<!-- part -->":
            part_mode = True
            index += 1
            continue
        if not stripped:
            flush()
            index += 1
            continue
        if stripped.startswith("|"):
            flush()
            table_flowables, consumed = parse_table(lines[index:], styles)
            flowables.extend(table_flowables)
            index += consumed
            continue
        if stripped.startswith("# "):
            flush()
            title = clean(stripped[2:])
            if part_mode:
                flowables.append(PageBreak())
                flowables.append(Spacer(1, 2.2 * 100))
                heading = book.SectionHeading(title, styles["part"])
                heading.toc_level = 0
                flowables.append(heading)
                headings.append((0, title))
                part_mode = "subtitle"
            else:
                flowables.append(PageBreak())
                heading = book.SectionHeading(title, styles["chapter"])
                heading.toc_level = 0
                flowables.append(heading)
                headings.append((0, title))
            index += 1
            continue
        if part_mode == "subtitle":
            flowables.append(Paragraph(clean(stripped), styles["part_sub"]))
            part_mode = False
            index += 1
            continue
        if stripped.startswith("## "):
            flush()
            flowables.append(Paragraph(clean(stripped[3:]), styles["h2"]))
            index += 1
            continue
        if stripped.startswith("### "):
            flush()
            flowables.append(Paragraph(clean(stripped[4:]), styles["h3"]))
            index += 1
            continue
        if stripped.startswith("- "):
            flush()
            flowables.append(Paragraph(clean(stripped[2:]), styles["bullet"], bulletText="\u2022"))
            index += 1
            continue
        import re
        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            flush()
            number = stripped.split(".", 1)[0] + "."
            flowables.append(Paragraph(clean(match.group(1)), styles["number"], bulletText=number))
            index += 1
            continue
        if is_book and path.name == "00-title.md":
            buffer.append(stripped)
            index += 1
            continue
        buffer.append(stripped)
        index += 1
    flush()
    return flowables, headings


def build_toc(entries: list, styles: dict) -> list:
    flowables = [Paragraph("Contents", styles["toc_head"])]
    for level, title, page in entries:
        label = clean(title)
        number = str(page) if page else "00"
        row = Table([[label, number]], colWidths=[BODY_W - 40, 40])
        row.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "PlainSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEADING", (0, 0), (-1, -1), 13),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#263a4a")),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        flowables.append(row)
    flowables.append(PageBreak())
    return flowables


def make_doc(path: Path, collector: list, toc_entries: list | None) -> None:
    doc = book.InteriorDoc(str(path), collector=collector, pagesize=(PAGE_W, PAGE_H),
                           leftMargin=LEFT, rightMargin=RIGHT, topMargin=TOP,
                           bottomMargin=BOTTOM,
                           title="Bio-Harmonization: review and editorial package",
                           author="Olabode Johnson Ilesanmi",
                           subject="Review package: manuscript, evidence audit and clinical review materials",
                           pageCompression=1)
    frame = book.Frame(LEFT, BOTTOM, BODY_W, PAGE_H - TOP - BOTTOM, id="main",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def draw_front(canvas, document):
        pass

    def draw_body(canvas, document):
        canvas.saveState()
        canvas.setFont("PlainSans", 7.5)
        canvas.setFillColor(colors.HexColor("#6b7781"))
        canvas.drawString(LEFT, PAGE_H - 0.58 * 100, "Review package · Bio-Harmonization")
        canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 0.58 * 100,
                               "Olabode Johnson Ilesanmi")
        canvas.setFont("PlainSans", 8.2)
        canvas.drawCentredString(PAGE_W / 2, 0.43 * 100, str(document.page))
        canvas.restoreState()

    doc.addPageTemplates([
        book.PageTemplate(id="front", frames=[frame], onPage=draw_front),
        book.PageTemplate(id="body", frames=[frame], onPage=draw_body),
    ])
    styles = make_styles()
    story: list = []
    all_files = REVIEW_FILES + [book.MANUSCRIPT / name for name in MANUSCRIPT_FILES] + EDITORIAL_FILES
    for index, path in enumerate(all_files):
        if index == 2:
            entries = toc_entries if toc_entries is not None else []
            story.append(book.NextPageTemplate("body"))
            story.extend(build_toc(entries, styles))
        flowables, _ = render_markdown(path, styles)
        story.extend(flowables)
    doc.build(story)


def main() -> None:
    book.register_fonts()
    entries: list = []
    for attempt in range(1, 6):
        collected: list = []
        make_doc(OUTPUT, collected, entries)
        if collected == entries:
            print(f"Contents stable after pass {attempt}")
            break
        entries = collected
    else:
        raise SystemExit("Contents did not stabilise")
    book.strip_unused_fonts(OUTPUT)
    print(f"Wrote {OUTPUT.name}: {OUTPUT.stat().st_size:,} bytes; sections: {len(entries)}")


if __name__ == "__main__":
    main()
