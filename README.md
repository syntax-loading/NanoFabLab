# LAB3 — Gate Formation (IH2659 / FIH3608 HT26)

Materials for the LAB3 process-flow deck and the lab record.

## Start here

- **The deck:** [`slides/lab3_process_flow.html`](slides/lab3_process_flow.html) —
  open it in a browser. Single self-contained file, no build step, no network.
- **Presenting it:** [`slides/SCRIPT.md`](slides/SCRIPT.md) is the narration, one
  section per page; [`slides/QnA.md`](slides/QnA.md) is the Q&A cheatsheet
  (44 likely questions, the numbers card, and the honest "not recorded" answers).
- **Deck documentation, editing guide and QA notes:**
  [`slides/README.md`](slides/README.md) — read this before editing anything:
  it lists where the copy lives, which numbers are measured, which visual
  choices are deliberate, and the URL hooks used for review (`?instant=1`,
  `?at=…`, `?qa=1`, `#n`).

## Layout

```
labs/
├── slides/
│   ├── lab3_process_flow.html   the deck (19 beats, ~15 min)
│   ├── QnA.md                   the Q&A cheatsheet
│   ├── README.md                how it works, where the copy is, what not to break
│   ├── .gitignore
│   └── _shot/                   contact-sheet renderer + the generated preview
├── assets/
│   ├── wafer_pattern/           top-view wafer pattern generator (inlined into the deck)
│   └── pattern/                 reference crops of one wafer cell
├── HT26 Lab 3/                  raw measurement files and the original micrographs
├── LAB3_checklist.{md,docx,pdf}      the lab checklist (EN variants too)
├── LAB3_record_v2.{md,tex,pdf}       the written lab record
├── LAB3_wafer_structure.svg          the stack drawing used in the record
└── build_checklist_docx*.py          scripts that rebuild the checklists
```

## Provenance of the numbers in the deck

| what | file |
|---|---|
| hard-mask thickness before the etch (5 points) | `HT26 Lab 3/SI WAFEFR.txt` |
| hard-mask thickness after the etch (5 points) | `HT26 Lab 3/HARDMASK 12 S bt 20 S mAIN.txt` |
| the three optical micrographs inlined in the deck | `HT26 Lab 3/*.jpg` (see `slides/README.md` for which one is which page) |

## Before you publish this repository

- `HT26 Lab 3/lab3.pdf` is KTH course material — keep it out of a public repo
  (or make the repo private).
- `slides/_shot/contact_sheet.png` is generated; regenerate it with
  `_shot/mk_sheet.sh` after any visual change rather than editing it.
- LaTeX intermediates (`*.aux`, `*.log`, `*.out`) and the PDF page cache are
  ignored by `.gitignore`.
