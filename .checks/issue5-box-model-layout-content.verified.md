# Issue #5 box model content Verification

**Verdict**: PASS
**Profile**: light (AGENTS.md declares none; default applies)
**Diff range**: 4a910b0..c23293c (HEAD of `fix/box-model-layout-content`)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Checks proven: 7 of 7. All proofs were run by the Verifier at `c23293c`; the working tree was clean before and after (`git status --porcelain` empty).

## Not run because of the profile

- Step 1, binding sources: `ui` only. The checklist marks no source binding. Issue #5 was read anyway (`gh issue view 5 --repo sh4wty1/squint-mcp --json title,body`): the checks match its defect and direction, and the user's decision (`content` = layout size, `box` = transformed rect) was taken as settled.
- `Coverage` join, `Test policy` verdicts: `standard`/`ui` only. The checklist carries neither section.
- Fault injection: `standard`/`ui` only. No mutant was run, so no proof here was seen to fail on a regression. See "Residual risk".

## Checks

Proofs for C1 to C5 ran in one invocation: `uv run pytest tests/test_inspect_element.py -v -k "<the five names>"` - 48 collected, 5 selected, 5 passed, exit 0, each name listed individually as PASSED. The four tests for C1 to C4 are added by the diff range (`tests/test_inspect_element.py` +26); the C5 test predates it, which is right for a "still reports" claim.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `#scaled` (border-box 100x60, border 5, padding 10px 20px, `scale(2)`) reports `boxModel.content == {"w": 50, "h": 30}` | `...::test_box_model_content_is_the_layout_size_of_a_scaled_element` PASSED | `tests/test_inspect_element.py:136` - `assert content["boxModel"]["content"] == {"w": 50, "h": 30}` for `#scaled` (`:135`); fixture `tests/fixtures/box.html:93-105` matches the claim's geometry | PASS |
| C2 | The same element reports `box == {"x": 40, "y": 1000, "w": 200, "h": 120}` | `...::test_box_of_a_scaled_element_is_the_transformed_rect` PASSED | `tests/test_inspect_element.py:141` - `assert content["box"] == {"x": 40, "y": 1000, "w": 200, "h": 120}`; `transform-origin: 0 0`, `top: 1000px`, `left: 40px` in `tests/fixtures/box.html:93-105` | PASS (see gap 4) |
| C3 | `#rotated` (same box, `rotate(90deg)`) reports `boxModel.content == {"w": 50, "h": 30}` | `...::test_box_model_content_is_the_layout_size_of_a_rotated_element` PASSED | `tests/test_inspect_element.py:148` - `assert content["boxModel"]["content"] == {"w": 50, "h": 30}` for `#rotated` (`:147`); fixture `tests/fixtures/box.html:107-118` | PASS |
| C4 | `#vector` (an `<svg>` of 40x20, no `offsetWidth`) reports `boxModel.content == {"w": 40, "h": 20}` | `...::test_box_model_content_of_an_svg_element_falls_back_to_its_rect` PASSED | `tests/test_inspect_element.py:155` - `assert content["boxModel"]["content"] == {"w": 40, "h": 20}` for `#vector` (`:154`); fixture `tests/fixtures/box.html:154` - `<svg id="vector" width="40" height="20">` | PASS (see gap 1) |
| C5 | `#solid` (no transform) still reports `boxModel.content == {"w": 80, "h": 40}` | `...::test_box_model_reports_margin_border_padding_and_content` PASSED | `tests/test_inspect_element.py:124-129` - `assert content["boxModel"] == {... "content": {"w": 80, "h": 40}}` for `#solid` (`:123`); test not touched by the diff, as a regression check should be | PASS |
| C6 | `docs/adr/0003-box-model-content-is-layout-size.md` exists and says `content` is the layout size while `box` is the transformed rect | `grep -c -i -E "layout size\|transformed rect" docs/adr/0003-box-model-content-is-layout-size.md` printed `3`, exit 0 | Read, not only grepped: `docs/adr/0003-box-model-content-is-layout-size.md:1` - "`boxModel.content` is the layout size; `box` is the transformed rect"; `:3` states both and the rejected alternative. File added by the diff | PASS (see gap 5) |
| C7 | Type check, lint, format and the whole suite are green | four commands, see Gate | exit 0 on each | PASS |

## Swept rows resolving to existing code

| Row | Cited | Found | Result |
|---|---|---|---|
| failure modes - an element with no `offsetWidth` would otherwise serialise `NaN` | C4 | `src/squint_mcp/js/collect_elements.js:20-21` - `element.offsetWidth ?? rect.width` / `element.offsetHeight ?? rect.height`; without the `??`, `undefined - border...` is `NaN` at `:34-35` | holds |

Rows marked *not in scope* are policy and were not judged.

## Gaps (ranked; none blocks the verdict)

1. **The issue's defect is still there for a transformed SVG or MathML element, and no check covers it.** `src/squint_mcp/js/collect_elements.js:20-21` falls back to the transformed rect and `:34-35` still subtracts untransformed border and padding from it. The checklist's Landing and `docs/adr/0003-box-model-content-is-layout-size.md:9` say so openly ("transform included"), and C4 pins only the untransformed case (`tests/fixtures/box.html:120-125`, no transform on `#vector`). Declared, not hidden - but it means issue #5 is fixed for HTML elements only.
2. **Sampling gap: only an element's own transform is tested.** `#scaled` and `#rotated` (`tests/fixtures/box.html:93-118`) carry the transform themselves. An untransformed element inside a transformed ancestor had the same defect; `offsetWidth` fixes it too, but no test pins it.
3. **Precision gap: the integer rounding has no check.** Landing and `collect_elements.js:19` say a fractional layout width is rounded in `content` and not in `box`. Every fixture is whole-pixel, so nothing asserts what a 100.5px box reports. This is a behaviour change for untransformed fractional elements, which the old rect-based code reported unrounded.
4. **C2 passes on the pre-fix code too.** `box` (`collect_elements.js:23-28`) was not changed by the diff, so `tests/test_inspect_element.py:141` is a regression guard, not evidence of the fix. That is what the claim asks for ("stays"), so it is a note, not a defect.
5. **C6's grep counts lines matching either phrase.** It would print 2 for a file that says "layout size" twice and never mentions the transformed rect. Settled here by reading `:1` and `:3`, which state both.
6. **The docstring change has no check.** Landing names the `inspect_element` docstring; `src/squint_mcp/tools/inspect_element.py:42-43` carries the new sentence, but nothing asserts it. It also says `boxModel` is "its layout, before" transforms without the SVG/MathML exception of gap 1.
7. **Stale citation outside the diff**: `.specs/features/capture-inspect-element/validation.md:49` cites `tests/test_inspect_element.py:121` for the `boxModel` literal; the assert is at `:124`. The checklist puts that spec's record out of scope.

## Residual risk

No fault was injected (profile `light`). By reading the old expression in the diff, C1 and C3 would have failed before the fix (150x70 and 10x70 against the asserted 50x30), and C4 would fail without the `??` fallback; none of that was observed by running a mutant.

## Gate

At `c23293c`:

- `uv run pyright` - 0 errors, 0 warnings, exit 0
- `uv run ruff check` - All checks passed, exit 0
- `uv run ruff format --check` - 45 files already formatted, exit 0
- `uv run pytest -v` - 60 passed, 0 failed in 46.54s, exit 0
