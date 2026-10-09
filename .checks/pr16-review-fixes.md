# PR #16 review fixes

Profile: light (none declared in `AGENTS.md`).

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/16#pullrequestreview-5471882870 - findings F1 to F4, with the repro and the fix each one asks for
- conversation - a direct test of `vision.count_limit` is accepted (the maintainer's answer to the question F1 ends on); its two minimum cases; the wording of F4; one atomic commit per finding; no push

## Out of scope

- Any check of `.specs/features/capture-pixel-budget/checks.md` (C1 to C15) - F1 adds a test, it changes no approved check
- Any other change to `vision.py`, to the fixtures or to the existing tests - decided by the user
- `docs/tasks/2026-10-08-capture-pixel-budget.md:11`, which also says the push waits for the maintainer - not one of the four findings; reported, not edited
- `git push` - waits for the user

## Landing

Touches `src/squint_mcp/vision.py` (one expression in `text_backgrounds`, one parameter name in `_countable`), a new `tests/test_vision.py`, `.specs/STATE.md` and `CHANGELOG.md`. Reuses `vision.area` instead of the sum it duplicates.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| A test that imports `vision` instead of going through the MCP client | `tests/test_vision.py`, `from squint_mcp.vision import count_limit`, plain `def test_...` with no fixture | a fixture page whose Finding depends on the cap, the convention today - the review shows two wrong caps survive all 64 such tests; a pure function is settled exactly by calling it. Decided by the maintainer |

- Nothing else in this change is hard to reverse

## Checks

### S1 - The cap is pinned (F1) · 2 files · 8 KB · ~2k

**C1** - `count_limit([100, 300_000, 300_000]) == 131022.0`: the text of 100 pixels is counted whole and the two others share what it leaves
Proof: `uv run pytest "tests/test_vision.py::test_a_text_under_the_limit_leaves_what_it_does_not_use_to_the_others" -v`

**C2** - `count_limit([100, 200]) == math.inf`: texts that all fit are not sampled
Proof: `uv run pytest "tests/test_vision.py::test_texts_that_fit_together_have_no_limit" -v`

**C3** - With `count_limit` returning a sixteenth of its value (`left / larger / 16` at `vision.py:60`), `tests/test_vision.py` fails
Proof: in a copy of `src/` with that one line changed, `PYTHONPATH=<copy>/src uv run pytest tests/test_vision.py` exits 1

**C4** - With `count_limit` returning `config.COLOR_COUNT_MAX_PIXELS / len(areas)` whatever the areas, `tests/test_vision.py` fails
Proof: in a copy of `src/` with the body replaced by that return, `PYTHONPATH=<copy>/src uv run pytest tests/test_vision.py` exits 1

### S2 - One area (F2) · 1 file · 7 KB · ~2k

**C5** - `text_backgrounds` takes `together` from `area(background, boxes)`
Proof: `grep -c "together = area(background, boxes)" src/squint_mcp/vision.py` prints 1
Proof: `grep -c "sum(region.width" src/squint_mcp/vision.py` prints 0

**C6** - The parameter of `_countable` is `together`; nothing in `vision.py` shadows `area`
Proof: `grep -c "def _countable(region: Image.Image, together: int, limit: float)" src/squint_mcp/vision.py` prints 1
Proof: `uv run pytest tests/test_low_contrast_real.py tests/test_inspect_element.py` (behaviour unchanged)

### S3 - Handoff and changelog (F3, F4) · 2 files · 9 KB · ~2k

**C7** - The Handoff of `.specs/STATE.md` names slice 7 (`offscreen-overflow`, `tlc-spec-lean`) as the next step, with no blocker and no open question
Proof: `grep -c "push waits\|once the maintainer\|precision gap 1" .specs/STATE.md` prints 0
Proof: `grep -c "Next step.*offscreen-overflow.*tlc-spec-lean" .specs/STATE.md` prints 1

**C8** - The `low-contrast-real` entry under Unreleased says a text of very little ink may not be judged on such a page
Proof: `grep -c "a text of very little ink may not be judged on such a page" CHANGELOG.md` prints 1

### S4 - Gate

**C9** - Type check, lint, format and the whole suite are green; no approved check, fixture or existing test changed
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`
Proof: `git diff --stat 0b4e767..HEAD -- tests/fixtures tests/conftest.py tests/helpers.py "tests/test_[!v]*.py" .specs/features/capture-pixel-budget/checks.md` prints nothing

## Swept

- validation: not in scope - `count_limit` takes areas the Check computes itself
- failure modes: C2 - no area over the budget returns `inf`, not a division
- idempotency: not in scope - a pure function
- authorization: not in scope
- concurrency: not in scope
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope - no log requirement

## Handoff

S1-S4 = ~6k of reading, one surface. One agent, no handoff.
