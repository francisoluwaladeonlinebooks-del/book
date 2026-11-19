# KDP submission checklist and metadata

## Interior file

- [x] File: `Bio-Harmonization-KDP-interior.pdf`, 95 pages, 6 × 9 in (432 × 648 pt).
- [x] One book page per PDF page. No two-page spreads.
- [x] No crop marks, trim marks, registration marks, bleed boxes or watermarks.
- [x] No standalone "Proof" text or other placeholder content.
- [x] Fonts embedded as subsets: DejaVu Serif, DejaVu Sans, DejaVu Sans Bold.
- [x] Margins: 0.88 in inner/left, 0.68 in outer/right, 0.86 in top, 0.78 in bottom.
- [x] Running heads and page numbers present from the contents onward.
- [x] Contents page numbers checked against the final pagination.
- [ ] Open every page in KDP Print Previewer and confirm nothing is clipped.
- [ ] Check that the title page, copyright page and disclaimer appear in the preview.

## Cover

The cover is a separate file and is not included here. For a 6 × 9 in trim with no bleed, the full cover size is 6.12 × 9.25 in (spine width depends on page count; KDP's cover calculator gives the exact value for the final paper choice). Use KDP's cover template after selecting paper and trim.

- [ ] Cover PDF created and checked in preview.
- [ ] Title and author spelling match the interior.

## Suggested metadata

Title: Bio-Harmonization: The Bureau Protocol
Author: Olabode Johnson Ilesanmi
Publisher / imprint: Olabode Johnson Ilesanmi
Language: English
Description: A practical guide to organising women's health information: what to record, how to spot patterns, how to prepare questions for an appointment, and where the evidence is still thin. Written by an information technology professional, not a clinician. Education only; no treatment claims.
Categories: Health, Fitness & Dieting > Women's Health; Health, Fitness & Dieting > Health Care Issues
Suggested keywords: women's health information, symptom tracking, health literacy, PCOS facts, perimenopause questions, patient advocacy, evidence and health
Age range: adult
Print edition ISBN: assign through KDP or supply your own.

## Content and disclosure

- [ ] Review KDP's current content guidelines before upload.
- [ ] Answer the AI-disclosure question accurately. This revision was produced with AI assistance that generated and edited text. If KDP asks whether AI was used to create text, answer yes and state that the author checked the sources and claims. Do not select "no" on the understanding that AI only helped with proofreading.
- [ ] Confirm the manuscript does not describe an institutional research programme, named clinicians or outcome data that do not exist. It does not.
- [ ] Confirm the copyright page names the individual author. It does.
- [ ] Complete the independent clinical review described in `clinical-review-packet.md`. Until then, do not use "medically reviewed" in the description or on the cover.
- [ ] Check that any testimonials or review quotes you add later are genuine and permitted.

## Before resubmission

1. Build the interior with `python3 book/build_interior.py`.
2. Inspect the PDF in KDP Print Previewer at full size.
3. Upload the interior and the separate cover.
4. Enter the metadata above and answer disclosure questions honestly.
5. Order a printed proof and inspect the physical copy before approving distribution.
