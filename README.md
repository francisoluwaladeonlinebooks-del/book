# Book production package: Bio-Harmonization: The Bureau Protocol

This folder contains the remediated manuscript and the files needed to rebuild the KDP print interior.

## Deliverables

- `Bio-Harmonization-KDP-interior.pdf`: the print interior. 95 single pages, 6 × 9 in, embedded fonts, no printer's marks, no "Proof" page.
- `Bio-Harmonization-Review-Package.pdf`: one 89-page US Letter PDF for reviewers and editors. It contains the full manuscript, review brief, evidence audit, edit report, clinical review packet, KDP checklist and a blank query log.
- `manuscript/`: editable markdown source, one file per front-matter item, chapter, part, appendix, references and author bio.
- `editorial/evidence-audit.md`: claim-by-claim audit of the uploaded proof, with what was removed, reframed or verified.
- `editorial/editorial-report.md`: chapter-by-chapter edit report and humanizer pass.
- `editorial/clinical-review-packet.md`: materials, checklist and blank sign-off form for independent clinical review. **No review has been completed.**
- `editorial/kdp-submission-checklist.md`: technical checks and suggested metadata.

## Rebuild

The build uses Python with `reportlab` and `pypdf`, and DejaVu fonts from `/usr/share/fonts/truetype/dejavu`.

```
python3 -m venv /tmp/bookvenv
/tmp/bookvenv/bin/pip install reportlab pypdf
/tmp/bookvenv/bin/python book/build_interior.py
/tmp/bookvenv/bin/python book/qa_interior.py
/tmp/bookvenv/bin/python book/build_review_package.py
```

The build performs three or four passes so the contents page numbers settle on the final pagination. It writes the PDF in place.

## Editorial status

The manuscript is technically ready for KDP preview. It is **not** ready to be described as medically reviewed. Obtain the signatures in the clinical review packet first, and check the AI-disclosure question honestly when uploading.
