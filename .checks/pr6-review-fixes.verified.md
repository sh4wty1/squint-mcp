# PR #6 review fixes Verification

**Verdict**: PASS
**Profile**: light (default - `AGENTS.md` declares none)
**Diff range**: 6fd84d9..12bdefb
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Steps run: 2 (every proof), 3 (assertions, `Swept` rows resolving to existing), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`), 4 (fault injection, `standard`, `ui`).

## Binding sources

None marked binding. The review (`pullrequestreview-5443894564`, state COMMENTED) and its three inline comments were opened with `gh api` and read as context only: F1, F2 and F3 each map to a check (F1 -> C1-C5, F2 -> C6, F3 -> C7), and the helper at `src/squint_mcp/js/collect_elements.js:23-24` is the expression the review proposes and the user settled on (option A).

## Checks

Tests C1-C4 ran in one invocation: `uv run pytest tests/test_inspect_element.py -v -k "<four names>"` - 4 selected, 4 PASSED, exit 0. Each name appears individually as PASSED.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `#frac` content is `{"w": 100.5, "h": 60}` | `...::test_box_model_content_keeps_the_fractional_size_of_an_untransformed_element PASSED` | `tests/test_inspect_element.py:162` - `assert content["boxModel"]["content"] == {"w": 100.5, "h": 60}` (test added in this range) | PASS |
| C2 | `#scaled` content still `{"w": 50, "h": 30}` | `...::test_box_model_content_is_the_layout_size_of_a_scaled_element PASSED` | `tests/test_inspect_element.py:136` - `assert content["boxModel"]["content"] == {"w": 50, "h": 30}` | PASS |
| C3 | `#rotated` content still `{"w": 50, "h": 30}` | `...::test_box_model_content_is_the_layout_size_of_a_rotated_element PASSED` | `tests/test_inspect_element.py:148` - `assert content["boxModel"]["content"] == {"w": 50, "h": 30}` | PASS |
| C4 | `#vector` content still `{"w": 40, "h": 20}` | `...::test_box_model_content_of_an_svg_element_falls_back_to_its_rect PASSED` | `tests/test_inspect_element.py:155` - `assert content["boxModel"]["content"] == {"w": 40, "h": 20}` | PASS |
| C5 | ADR-0003 says the rect is kept within 1px of the offset size | `grep -c "within 1px" docs/adr/0003-box-model-content-is-layout-size.md` -> `1` | `docs/adr/0003-box-model-content-is-layout-size.md:8` - "The rect is kept when it is within 1px of them" | PASS |
| C6 | Description limits "layout, before transforms" to HTML elements | `grep -c "for HTML elements" src/squint_mcp/tools/inspect_element.py` -> `1` | `src/squint_mcp/tools/inspect_element.py:43-44` - "`boxModel` is its layout, before them, for HTML elements." | PASS |
| C7 | Issue #5 report cites 150x90, not 150x70 | `grep -c "150x70" ...verified.md` -> `0`; `grep -c "150x90" ...verified.md` -> `1` | `.checks/issue5-box-model-layout-content.verified.md:51` - "(150x90 and 10x70 against the asserted 50x30)" | PASS |
| C8 | Type check, lint, format, whole suite green | see Gate | - | PASS |

C2, C3 and C4 resolve to tests this range did not touch. They are regression proofs over code the range did change (`collect_elements.js:23-26`), so they still bear on the new behaviour.

## Swept rows resolving to existing

| Row | Cited constraint | In the code |
|---|---|---|
| failure modes: C4 - no `offsetWidth` must not serialise `NaN` | `offset === undefined` guard | yes - `src/squint_mcp/js/collect_elements.js:24`, `offset === undefined \|\| Math.abs(painted - offset) < 1 ? painted : offset` |

All other rows say *not in scope* and were not judged.

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section either.

## Faults injected

Skipped by profile. Nothing below was observed by running a mutant.

## Gaps and notes (ranked)

1. No discrimination evidence (profile limit, not a failure). That C1 fails under the pre-fix `offset ?? painted` (101 instead of 100.5) rests on the review's reproduction and on reading the diff, not on a mutant run here. Same for C2/C3 catching a helper that always returns `painted`.
2. Coverage narrower than the review's repro. The review names three untransformed fractional cases (a 100.5px div, an inline span at 111.172, a `td` at 49.25); only the div has a test. The review itself asks for just "a `#frac` fixture with one test", so the checklist matches the ask.
3. The review says the fix "drops the `ponytail:` ceiling". The code keeps a `ponytail:` comment at `collect_elements.js:21-22`, now naming a different ceiling (a transform under 1px is read as none). The checklist's `Landing` declares that ceiling, so this is a deviation from the review's wording, not from the checklist.
4. The sub-1px-transform ceiling and a fractional element under a transform have no test. Both are declared in `Landing` / `Out of scope`; recorded, not judged.
5. C5, C6 and C7 are grep proofs: they prove the phrase is present, not that the surrounding prose is right. The cited lines were read and do say what the checks claim.

## Gate

At 12bdefb, working tree clean before and after:

- `uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
- `uv run ruff check` - All checks passed!, exit 0
- `uv run ruff format --check` - 47 files already formatted, exit 0
- `uv run pytest` - 61 passed, 0 failed
