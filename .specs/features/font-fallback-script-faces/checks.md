# font-fallback: Faces added by a script - checks

Profile: light

## Intent

Review F1 of pull request #29 (issue #20). `document.fonts` gives the name of a Face of an `@font-face` rule as written, and the name of a Face a script adds with `new FontFace` CSS-serialized: `"Script Face"` with its quotation marks, `"Back\\slash"` with its escapes (Chromium 153, the reviewer's probe). Since F5 the name of a Face is taken as given, so a failed script Face whose name needs quoting gets no Finding: `#spaced` of `font-family: "Script Face", Ahem` was reported on `main` and is not on the head of #29. The string cannot tell the two origins apart (a rule's Face named `"Quoted"`, FNT-64, reads as a serialized one), and the maintainer chose on 2026-10-17 to match both: a Face answers to its name as given and to that name decoded, the name as given winning where two Faces would take one name, and the Finding names the family as it matched. The known limit, labeled `ponytail:` in `font_widths.js`: a failed rule's Face whose name reads as a serialized one also catches another family that has its decoded name. With this, a failed script Face is reported whatever characters its name holds, and every case of FNT-63 to FNT-67 keeps its Finding.

Review F2: the CHANGELOG entry of #20 names the backslash and quotation-mark names, links #20, and the Fixed list has no blank line in it.

4 checks in 1 slice · 0 one-way doors · 0 open

## Checks

### S1 - Script Faces and the changelog · 6 files · 52 KB · ~13k

**C1** - A failed Face added with `new FontFace("Script Face", ...)`, on `#script-face` of `font-family: "Script Face", Ahem` in `font-fallback-names.html`, gets one Finding on `#script-face` with `evidence.measured.family` equal to `Script Face`, no quotation marks (F1)
Proof: `uv run pytest tests/test_font_fallback.py -k "test_a_family_a_script_adds_is_reported_under_its_name"`

**C2** - A failed Face added with `new FontFace("Script\\Slash", ...)` (one backslash in the name), on `#script-slash` of `font-family: "Script\\Slash", Ahem`, gets one Finding on `#script-slash` with `evidence.measured.family` equal to `Script\Slash`, one backslash (F1)
Proof: `uv run pytest tests/test_font_fallback.py -k "test_a_family_a_script_adds_is_reported_under_its_name"`

**C3** - The Faces of rules keep the Findings of FNT-60 and FNT-63 to FNT-67 under the names they had: `Vinyl 12"`, `Back\slash`, `"Quoted"` with its quotation marks, `'Single'` with its apostrophes, the three whitespace names and the two escape names (F1, no regression)
Proof: `uv run pytest tests/test_font_fallback.py -k "written_with_a_backslash or holds_a_backslash or quotation_mark_keeps_it or apostrophe_keeps_it or whitespace_that_belongs or hexadecimal_escape"`

**C4** - The `### Fixed` list of `[Unreleased]` in `CHANGELOG.md` has no blank line between its entries, and its `font-fallback` entry names backslashes, quotation marks and Faces a script adds, and links `https://github.com/sh4wty1/squint-mcp/issues/20` (F2)
Proof: `uv run python -c "import re,sys; s=open('CHANGELOG.md',encoding='utf-8').read(); f=s.split('### Fixed',1)[1].split('\n## ',1)[0].strip(); e=[l for l in f.split('\n') if 'font-fallback' in l]; sys.exit(not ('\n\n' not in f and len(e)==1 and all(w in e[0] for w in ('backslash','quotation mark','script','issues/20'))))"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| origin of a Face (2) | `@font-face` rule C3 · `new FontFace` C1 | - |
| what the serialization of a script Face adds (2) | quotation marks C1 · backslash escape C2 | - |
| names of rules that read as serialized (3) | `"Quoted"` C3 · `'Single'` C3 · `Back\slash` C3 | - |
| review findings (2) | F1 C1 · F2 C4 | - |

- No check claims more than the cases its proof exercises

## Swept

- validation: n/a - the names come from the page's own `document.fonts` and computed styles, nothing is parsed from a caller
- failure modes: C1, C2
- idempotency: n/a - a Capture reads, it writes nothing
- authorization: n/a - no access control in a Check
- concurrency: n/a - one evaluation in one page
- data lifecycle: n/a - nothing is stored
- dependency failure: n/a - a Face that fails is the input itself, not a dependency of the Check
- state transitions: n/a - no state
- observability: n/a - no logging in a Check

## Out of scope

- Telling a script Face from a rule's Face exactly (wrapping the page's `FontFace`) - rejected by the maintainer on 2026-10-17: it changes a global of the page
- Case folding beyond `toLowerCase` (final sigma) - the accepted limit of FNT-67

## Handoff

- S1 = `font_widths.js` 5 KB + `font_fallback.py` 3 KB + `models.py` 6 KB + `font-fallback-names.html` 6 KB + `test_font_fallback.py` 23 KB + `CHANGELOG.md` 10 KB = 52 KB / 4 = ~13k - one builder
