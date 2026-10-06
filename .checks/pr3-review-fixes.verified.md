# PR #3 review fixes Verification

**Verdict**: PASS
**Profile**: light (AGENTS.md declares none; default applies)
**Diff range**: 9e3353f..e217bc6 (HEAD of `feat/capture-inspect-element`)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Checks proven: 8 of 8. All proofs were run by the Verifier at `e217bc6`; the working tree was clean before and after (`git status --porcelain` empty).

## Not run because of the profile

- Step 1, binding sources: `ui` only. The checklist marks no source binding. The PR review comments were read anyway (`gh api repos/sh4wty1/squint-mcp/pulls/3/comments`) to compare each claim with its finding; C1 to C7 each match the repro and the fix the finding asks for.
- `Coverage` join, `Test policy` verdicts: `standard`/`ui` only. The checklist carries neither section.
- Fault injection: `standard`/`ui` only. No mutant was run, so no proof here was shown to fail on a regression. See "Residual risk".

## Checks

Proofs for C1 to C7 ran in one invocation: `uv run pytest tests/test_inspect_element.py -v -k "<the five names>"` - 5 selected, 5 passed, exit 0, each name listed individually as PASSED. All five tests are added by the diff range (`tests/test_inspect_element.py` +64).

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `#left-of-page` (`left: -9999px`) is a tool error with the no-rendered-box message | `...::test_element_outside_the_page_origin_has_no_rendered_box` PASSED | `tests/test_inspect_element.py:363` - `assert f'Selector "{selector}" matched an element with no rendered box.' in text`, looped over `("#left-of-page", "#above-page")` at `:361`; tool error at `:335` - `assert result.is_error is True`; fixture `tests/fixtures/box.html:78-81` | PASS |
| C2 | Same for `#above-page` (`top: -9999px`) | same test, same run | `tests/test_inspect_element.py:361-363` (second loop member); fixture `tests/fixtures/box.html:85-87` | PASS |
| C3 | 100s opacity animation running inside an open shadow root reports `computed.opacity == "1"` | `...::test_animations_inside_an_open_shadow_root_are_taken_to_their_end` PASSED | `tests/test_inspect_element.py:208` - `assert content["computed"]["opacity"] == "1"` for `#shadow-animated` (`:207`); fixture `tests/fixtures/motion.html:52-53` - `animation: fade 100s forwards` inside `<template shadowrootmode="open">` | PASS |
| C4 | 100s opacity transition inside an open shadow root starting 300ms after `load` reports `computed.opacity == "1"` | `...::test_transitions_starting_later_inside_an_open_shadow_root_take_no_time` PASSED | `tests/test_inspect_element.py:215` - `assert content["computed"]["opacity"] == "1"` for `#shadow-late` (`:214`); precondition at `tests/fixtures/motion.html:57` (`transition: opacity 100s`) and `:73-76` (`setTimeout(..., 300)`) | PASS (see gap 2) |
| C5 | `stabilize.js` comment and the "Zeroing animations" row of `design.md` no longer say `document.getAnimations()` reaches shadow trees | `grep -n -E "also reaches open shadow trees\|covers shadow trees" src/squint_mcp/js/stabilize.js .specs/features/capture-inspect-element/design.md` - no hit, exit 1 | Read, not only grepped: `src/squint_mcp/js/stabilize.js:6-7` - "Neither a style nor getAnimations() crosses a shadow boundary"; `.specs/features/capture-inspect-element/design.md:227` - "Neither crosses a shadow boundary, so each open shadow root gets both" | PASS (see gap 3) |
| C6 | After the client cancels a call to a URL that never answers, 1.5s in, the browser has 0 open contexts within 3s | `...::test_call_cancelled_by_the_client_leaves_no_browser_context_open` PASSED | `tests/test_inspect_element.py:429` - `with anyio.move_on_after(1.5) as cancelled:`; `:431` - `assert cancelled.cancelled_caught`; `:432` - `with anyio.move_on_after(3):`; `:435` - `assert browsers[-1].contexts == []` | PASS (see gap 1) |
| C7 | After the cached Chromium is closed, the next call succeeds (`isError: false`, `box.w == 120` for `#solid`) | `...::test_call_after_the_browser_died_relaunches_it` PASSED | `tests/test_inspect_element.py:442` - `await browsers[-1].close()`; `:443` - `assert (await inspect(own, BOX, "#solid"))["box"]["w"] == 120`; `isError` at `:71` - `assert result.is_error is False, texts(result)` inside `inspect` | PASS |
| C8 | Type check, lint, format and the whole suite are green | four commands, see Gate | exit 0 on each | PASS |

## Swept rows resolving to existing code

| Row | Cited | Found | Result |
|---|---|---|---|
| concurrency - liveness test inside the existing `self._lock` | `capture.py:34` | `src/squint_mcp/capture.py:34` `async with self._lock:`; the test `not self._browser.is_connected()` is at `:36`, inside it | holds |
| dependency failure - failed relaunch keeps `Could not launch Chromium` | `capture.py:41-45` | `src/squint_mcp/capture.py:42-46` (`except PlaywrightError` ... `raise ToolError("Could not launch Chromium: ...")`); the relaunch goes through the same `try` at `:37` | holds; the citation is off by one line (the F4 comment at `:35` shifted it) |

Rows marked *not in scope* are policy and were not judged.

## Gaps (ranked; none blocks the verdict)

1. **C6 does not assert that a context was open when the call was cancelled.** The test asserts only the end state (`contexts == []`). A cancellation landing before `browser.new_context` (`capture.py:85`) would pass with the shield removed. At 1.5s into `/hang` the context is almost certainly open (the reviewer's repro saw 1 context without the fix), but the test does not pin it, and with fault injection out of profile nobody independent has seen this proof go red.
2. **C4 precision gap: "after stabilization ran" is a timing assumption, not an assertion.** It holds only if `load` plus `page.evaluate(_STABILIZE)` (`capture.py:94-97`) finish in under 300ms. On a slow machine the transition would already be running and `finish()` would end it instead of the injected style; the test stays green either way, so it proves shadow-root coverage but not specifically the injected-style path the claim names.
3. **C5's proof is a negative grep for two exact phrases.** It would pass for any rewording of the false statement. Settled here by reading both passages, which now state the opposite.
4. **Stale line citation in `Swept`**: `capture.py:41-45` is now `42-46`.

## Residual risk

No fault was injected (profile `light`), so discrimination of the five new tests rests on the author's test-first claim and on the reviewer's repros matching the tests, not on an observed failure.

## Gate

At `e217bc6`:

- `uv run pyright` - 0 errors, 0 warnings, exit 0
- `uv run ruff check` - All checks passed, exit 0
- `uv run ruff format --check` - 42 files already formatted, exit 0
- `uv run pytest -v` - 56 passed, 0 failed in 41.81s, exit 0
