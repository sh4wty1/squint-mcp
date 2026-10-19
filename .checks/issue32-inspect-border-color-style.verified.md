# Issue #32 - `inspect_element` border colour and style Verification

**Verdict**: PASS
**Profile**: light (the project declares none)
**Diff range**: main (1a8378b)..HEAD (90506a8)
**Round**: 1 - full, verified at 90506a8
**Verifier**: independent sub-agent (author != verifier)

## Binding sources

Step 1 not run under `light`. Issue #32 was opened (`gh issue view 32`) to check the scope only. It asks for the eight longhands `border-{top,right,bottom,left}-{color,style}` in `computed`, a fixture test and a CHANGELOG entry. The checklist matches this, and no check contradicts the issue.

## Checks

Proof batch: `uv run pytest tests/test_inspect_element.py -v -k "test_computed_holds_the_colour_of_each_border or test_computed_holds_the_style_of_each_border or test_computed_holds_the_border_of_a_default_button or test_computed_holds_exactly_the_configured_properties"`. It exited 0 with 4 passed and 54 deselected. Each test is listed as PASSED by name.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `#borders` colours red/green/blue/orange | `::test_computed_holds_the_colour_of_each_border` PASSED | `tests/test_inspect_element.py:189-192` - `assert computed["border-top-color"] == "rgb(255, 0, 0)"`, `...["border-right-color"] == "rgb(0, 128, 0)"`, `...["border-bottom-color"] == "rgb(0, 0, 255)"`, `...["border-left-color"] == "rgb(255, 165, 0)"` | PASS |
| C2 | `#borders` styles solid/dashed/dotted/double | `::test_computed_holds_the_style_of_each_border` PASSED | `tests/test_inspect_element.py:197-200` - `assert computed["border-top-style"] == "solid"`, `...["border-right-style"] == "dashed"`, `...["border-bottom-style"] == "dotted"`, `...["border-left-style"] == "double"` | PASS |
| C3 | default `<button>` top style `outset` | `::test_computed_holds_the_border_of_a_default_button` PASSED | `tests/test_inspect_element.py:205` - `assert computed["border-top-style"] == "outset"` (target `#button` at :204, an unstyled `<button>` in `box.html` that only sets its position) | PASS |
| C4 | default `<button>` top colour `rgb(0, 0, 0)` | same test PASSED | `tests/test_inspect_element.py:206` - `assert computed["border-top-color"] == "rgb(0, 0, 0)"` | PASS |
| C5 | exactly 20 old keys + 8 border keys = 28 | `::test_computed_holds_exactly_the_configured_properties` PASSED; `git diff main..HEAD -- tests/test_inspect_element.py \| grep -E "^-[^-]"` returned no line (exit 1) | `tests/test_inspect_element.py:177` - `assert set(content["computed"]) == COMPUTED_PROPERTIES`. The literal set at :28-57 has 28 entries, compared with 20 at `main`. The diff only adds the eight border lines (+:49-56). | PASS |
| C6 | CHANGELOG entry under `## [Unreleased]` names `border-*-style` | `grep -n "border-\*-style" CHANGELOG.md` gives line 11 | `CHANGELOG.md:11` (an `### Added` bullet) sits between `## [Unreleased]` at :7 and `## [0.1.0] - 2026-10-08` at :30 | PASS |
| C7 | pyright, ruff check, ruff format, full suite green | `uv run pyright`: 0 errors, exit 0. `uv run ruff check`: All checks passed, exit 0. `uv run ruff format --check`: 135 files already formatted, exit 0. `uv run pytest`: 527 passed in 1308.88s, exit 0 | the tool outputs given here | PASS |

The proofs touch new code. C1-C4 are new tests in this diff. C5's test existed before, but its expected set was extended in this diff.

Precision note (not a gap): C5's expected values sit in a module-level literal 150 lines above the assertion. It is still a plain literal set in the same file, so I could read it directly.

## Swept (existing)

| Row | Cited constraint | Found |
|---|---|---|
| failure modes | `config.py` `*INSPECT_COMPUTED_PROPERTIES` is the head of the Capture list, so no inspect name can be missing from a Capture's `computed` | `src/squint_mcp/config.py:88` `*INSPECT_COMPUTED_PROPERTIES,` opens `CAPTURE_COMPUTED_PROPERTIES`. At runtime `CAPTURE[:28] == INSPECT` and the two lists hold 28/28 and 40/40 unique names, so nothing is collected twice. `src/squint_mcp/tools/inspect_element.py:88` reads `element.computed[name] for name in config.INSPECT_COMPUTED_PROPERTIES`. Confirmed. |

The other Swept rows are `not in scope`, so there is nothing to check for them.

## Test policy rows / Coverage / Faults injected

Not run under `light`.

## Gate

- `uv run pytest`: 527 passed, 0 failed (exit 0)
- `uv run pyright`: 0 errors
- `uv run ruff check`: clean
- `uv run ruff format --check`: clean
