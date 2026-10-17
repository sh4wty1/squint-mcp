# font-fallback: Faces added by a script - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 1a00d9f..c27ce2e
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | failed `new FontFace("Script Face", ...)` on `#script-face` gets one Finding, `family` = `Script Face` without quotes | `.venv/bin/python -m pytest tests/test_font_fallback.py -v -k "test_a_family_a_script_adds_is_reported_under_its_name or ..."` exit 0, `test_a_family_a_script_adds_is_reported_under_its_name PASSED` | `tests/test_font_fallback.py:613` - `assert await reported(client, NAMES, families=families, on=on) == [("#script-face", "Script Face"), ("#script-slash", "Script\\Slash")]` | PASS |
| C2 | failed `new FontFace("Script\\Slash", ...)` on `#script-slash` gets one Finding, `family` = `Script\Slash` (one backslash) | same invocation, same test PASSED | `tests/test_font_fallback.py:615` - `("#script-slash", "Script\\Slash")` inside the list equality at :613 (Python literal = one backslash) | PASS |
| C3 | Faces of rules keep the Findings of FNT-60, FNT-63 to FNT-67 under the names they had | same invocation: `..._written_with_a_backslash_...`, `..._holds_a_backslash_...`, `..._quotation_mark_keeps_it`, `..._apostrophe_keeps_it`, `test_whitespace_that_belongs_...`, `..._hexadecimal_escape_...` all PASSED | `tests/test_font_fallback.py:553` - `== [("#inch", 'Vinyl 12"')]`; `:564` - `== [("#slash", "Back\\slash")]`; `:573` - `== [("#quoted", '"Quoted"')]`; `:582` - `== [("#single", "'Single'")]`; `:590` - list of the three whitespace names; `:602` - `[("#tab-name", "Tab\tName"), ("#unit-sep", "Unit\u001f Sep")]` | PASS |
| C4 | `### Fixed` of `[Unreleased]` has no blank line between entries; its `font-fallback` entry names backslashes, quotation marks, script Faces and links issue 20 | `.venv/bin/python -c "<the C4 one-liner from checks.md>"` exit 0 | `CHANGELOG.md:24` - entry holds `backslash`, `quotation marks`, `script adds`, `https://github.com/sh4wty1/squint-mcp/issues/20`; `CHANGELOG.md:23-26` - four consecutive `- ` lines, no blank line | PASS |

Run: 7 passed, 52 deselected in 24.83s (one invocation, `-v`, each named test listed individually). Every name in the `-k` expression matched a test (`rg -n` hits at `tests/test_font_fallback.py:549, 560, 569, 578, 587, 597, 608`).

## Level and sampling

- Level: all four proofs sit at the right boundary. C1-C3 go through `detect` over MCP against a real Chromium page (`reported` at `tests/test_font_fallback.py:189`), and assert `evidence.measured.family` via the Finding, which is what the claims name. C4 reads the file the claim is about.
- Sampling: C1 and C2 share one test, one list-equality assertion. Both values are readable at the assertion and both are asserted, so each claim is settled; a failure would not say which of the two broke. Not a gap.
- C3 runs only tests the diff did not touch. That is right for a no-regression claim (the change to `font_widths.js` is in the path of every one of them), but it proves nothing new: the new behaviour rests on C1/C2 alone.
- Discrimination (read, not injected): at `1a00d9f` the Face name was taken as given only, so `"Script Face"` (serialized) never matched `bare(names[0])` = `Script Face`; the C1/C2 test would fail there, which matches the reviewer's repro in F1.

## Swept existing

None: every `Swept` row in `checks.md` is `n/a` or names checks (C1, C2). Nothing to re-read against the code.

## Intent vs code

Read `src/squint_mcp/js/font_widths.js:52-70, 117-119` and `src/squint_mcp/checks/font_fallback.py:43-60` at HEAD.

- "A Face answers to its name as given and to that name decoded": holds. The loop at `font_widths.js:63` runs `(name) => name` then `bare` over every Face, adding both keys to `failed` for a failed Face.
- "The name as given winning where two Faces would take one name": holds. The as-given pass runs over all Faces before any decoded one, and `named` keeps the first entry per key (`if (!named.has(key))`).
- "The Finding names the family as it matched": holds. `font_widths.js:119` reads `family = named.get(key)`, and `font_fallback.py:59` now groups by `widths.family` as given. The Python `failed` filter and `names` map removed from `font_fallback.py` were redundant: the JS only emits `line_widths` for an element whose key is in `failed`, and every element of one key gets the same `named` string, so grouping is unchanged.
- Gap (minor, unlabeled ceiling): the `ponytail:` note names one direction only, a failed rule Face reading as serialized catching its decoded family. The mirror also holds and is not labeled: a failed script Face `Script Face`, whose name as given is `"Script Face"` with quotation marks, also catches text that asks for a family literally named `"Script Face"` (CSS `font-family: '"Script Face"'`), and that Finding names the family with its quotation marks. Same string ambiguity the Intent accepts, so not a defect of the claim; the label at `font_widths.js:57-60` just understates it. Neither direction has a test, which the checks accept (no check claims the limit).
- Note: `named` is filled from Faces of every status, so a loaded Face of the same key can give the reported name. That is the pre-existing "named as the first of its Faces has it" rule, not new.

## Gate

`.venv/bin/python -m pytest tests/test_font_fallback.py -v -k "<C1-C3 names>"` - 7 passed, 0 failed; C4 one-liner exit 0. Full suite not run (another process is running it).
