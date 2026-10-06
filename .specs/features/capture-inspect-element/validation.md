# Capture + inspect_element Validation

## Validation: capture-inspect-element - FAIL ❌

**Date**: 2026-10-06
**Spec**: `.specs/features/capture-inspect-element/spec.md`
**Diff range**: `main..HEAD` on `feat/capture-inspect-element` (14 commits, HEAD `80577bf`)
**Verifier**: independent sub-agent (author ≠ verifier), iteration 2 of at most 3

This is iteration 2, following a FAIL in iteration 1. All five gaps of iteration 1 are closed: its four blocking mutants and the viewport-height mutant are now killed, and CAP-46 is met. No product defect was found in either iteration.

The verdict is still FAIL, on test strength only. Two new mutants that contradict the text of a criterion pass the whole suite:

- **N9 (CAP-21)**: the network-idle wait cut from 3s to 1s. A page that goes idle after 2s is "within 3 seconds", yet the mutant reports `stabilized: false` for it.
- **N11 (CAP-35)**: the timeout message without its `:g` format. With the real default (`30.0`) it reads `Timed out after 30.0s`, not `Timed out after 30s`. The test patches the timeout with the integer `1`, so it cannot see this.

Both are closed by test-only changes of a few lines (Fix 1 and Fix 2). Six further survivors are flagged without blocking: no criterion defines the outcome they break.

How each claim was checked is marked **ran** (executed, output read) or **read** (file evidence only). Line numbers are from the files at `80577bf`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 Dependencies | ✅ Done | - |
| T2 Config defaults | ✅ Done | - |
| T3 Capture + tool | ✅ Done | - |
| T4 Crop + sampled colours | ✅ Done | - |
| T5 Clear errors | ✅ Done | - |
| T6 Total timeout | ✅ Done | - |
| T7 Chromium in CI | ✅ Done | - |
| T8 Documents | ✅ Done | README fixed in `85ed203` |
| Iteration-1 fixes 1 to 5 | ✅ Done | `85ed203`, `cbf5164` |

`tasks.md` has 35 ticked boxes and 0 unticked (ran grep).

---

## Spec-Anchored Acceptance Criteria

All test rows were executed in the full suite (50 passed). `T` = `tests/test_inspect_element.py`.

### P1: Inspect one element

| ID | Spec-defined outcome | `file:line` + assertion | Verdict |
| -- | -------------------- | ----------------------- | ------- |
| CAP-01 | exactly two tools, `ping` and `inspect_element` | `tests/test_ping.py:36` - `assert sorted(tool.name for tool in tools) == ["inspect_element", "ping"]` | ✅ |
| CAP-02 | `readOnlyHint: true`, `openWorldHint: true` | `tests/test_inspect_element.py:87` - `annotations.read_only_hint is True`; `tests/test_inspect_element.py:88` - `annotations.open_world_hint is True` | ✅ |
| CAP-03 | properties exactly `url`, `selector`, `viewport`; first two string and required; `viewport` object or null | `tests/test_inspect_element.py:96` - `set(properties) == {"url", "selector", "viewport"}`; `:97`, `:98` - `["type"] == "string"`; `:99` - `set(schema["required"]) == {"url", "selector"}`; `:106` - viewport types `== {"object", "null"}` | ✅ |
| CAP-04 | keys exactly the six documented | `tests/test_inspect_element.py:226` - `assert set(content) == {...six keys...}` | ✅ |
| CAP-05 | `box == {x:40, y:60, w:120, h:70}` | `tests/test_inspect_element.py:114` - `assert content["box"] == {"x": 40, "y": 60, "w": 120, "h": 70}` | ✅ |
| CAP-06 | the exact `boxModel` literal | `tests/test_inspect_element.py:121` - `assert content["boxModel"] == {...}`, literal equal to the spec's | ✅ |
| CAP-07 | exactly the 20 properties | `tests/test_inspect_element.py:131` - `set(content["computed"]) == COMPUTED_PROPERTIES` (`:23-44`, held in the test independently of `config`) | ✅ |
| CAP-08 | `20px`, `rgb(255, 0, 0)`, `block` | `tests/test_inspect_element.py:136`, `:137`, `:138` | ✅ |
| CAP-09 | `[{#ff0000, 0.7857}, {#0000ff, 0.2143}]` | `tests/test_inspect_element.py:238` - same literal | ✅ |
| CAP-10 | exactly 3 entries, share descending | `tests/test_inspect_element.py:246` - exact list of three (stronger than the spec) | ✅ |
| CAP-11 | computed white, first sampled `#000000` | `tests/test_inspect_element.py:257`, `:258` | ✅ |
| CAP-12 | `isError: false`, a text block with the selector, exactly one `image/png` | `tests/test_inspect_element.py:263`, `:264`, `:266` - `[image.mime_type for image in images] == ["image/png"]` | ✅ |
| CAP-13 | crop 152×102, 1:1, showing page background, blue border, red fill | `tests/test_inspect_element.py:272` - `crop_size(...) == (152, 102)`; `:277` - `getpixel((0, 0)) == (255, 255, 255)`; `:278` - `getpixel((16, 16)) == (0, 0, 255)`; `:279` - `getpixel((21, 21)) == (255, 0, 0)`; `:280` - centre red | ✅ (iteration-1 gap closed, R1 killed) |
| CAP-14 | crop 66×66 | `tests/test_inspect_element.py:284` - `== (66, 66)` | ✅ |
| CAP-15 | crop 512×65 | `tests/test_inspect_element.py:288` - `== (512, 65)` | ✅ |
| CAP-16 | viewport 1440×900, `#full` `box.w == 1440`, `#screen` `box.h == 900` | `tests/test_inspect_element.py:143`, `:144`, `:145` | ✅ |
| CAP-17 | viewport echoed, `#full` `box.w == 390`, `#screen` `box.h == 844` | `tests/test_inspect_element.py:151`, `:152`, `:154` | ✅ (iteration-1 gap closed, R5 killed) |
| CAP-18 | `null` equals omission | `tests/test_inspect_element.py:159` - `inspect(..., viewport=None) == omitted` | ✅ |
| CAP-19 | shadow-root element, `color == rgb(0, 0, 255)` | `tests/test_inspect_element.py:164` | ✅ |
| CAP-20 | `box.y == 2000`, first sampled `#008000`, scrolled or not | `tests/test_inspect_element.py:293`, `:294` (unscrolled); `:302`, `:303` (`box.html#below`) | ✅ (iteration-1 gap closed, R2 killed) |

### P1: Stabilized, isolated Capture

| ID | Spec-defined outcome | Evidence | How | Verdict |
| -- | -------------------- | -------- | --- | ------- |
| CAP-21 | `stabilized: true` when idle within 3s | `tests/test_inspect_element.py:168` - `["stabilized"] is True` | ran | ❌ assertion matches, but only for a page that is idle at once: a 1s bound also passes (N9 survives) |
| CAP-22 | `isError: false`, `stabilized: false` when not idle within 3s, including idle only after 5s | `tests/test_inspect_element.py:175` (never idle), `:182` (idle after 5s) - `is False`; `:68` - `result.is_error is False` | ran | ✅ (iteration-1 gap closed, R4 killed) |
| CAP-23 | `opacity == "1"` for animated and transitioned | `tests/test_inspect_element.py:188`, `:189` | ran | ✅ |
| CAP-24 | `document.fonts.ready` after `load`, before zeroing | `src/squint_mcp/capture.py:93` (`wait_until="load"`), `src/squint_mcp/capture.py:96`, `src/squint_mcp/js/stabilize.js:4` ahead of `src/squint_mcp/js/stabilize.js:7` | read | ✅ |
| CAP-25 | http, https, file accepted | `file://`: `tests/test_inspect_element.py:114`; `http://`: `tests/test_inspect_element.py:196`; `https`: `src/squint_mcp/capture.py:79` | ran + read | ✅ |
| CAP-26 | both calls report `rgb(0, 128, 0)` | `tests/test_inspect_element.py:203`, inside `for _ in range(2)` (`:201`) | ran | ✅ |
| CAP-27 | tools listed and `ping` answers without Chromium | `tests/test_inspect_element.py:354`, `:356`; fixture `tests/conftest.py:35` | ran | ✅ |
| CAP-28 | Chromium launched at most once | `src/squint_mcp/capture.py:34` (lock), `src/squint_mcp/capture.py:35` (`if self._browser is None`), `src/squint_mcp/capture.py:40`, `src/squint_mcp/server.py:11` | read | ✅ |
| CAP-29 | context closed on every exit path | `src/squint_mcp/capture.py:88` `try` … `src/squint_mcp/capture.py:115` `finally` / `:116` `await context.close()`; `src/squint_mcp/tools/inspect_element.py:49` `asyncio.timeout` | read | ✅ |

### P1: Clear errors

| ID | Spec-defined text | `file:line` + assertion | Verdict |
| -- | ----------------- | ----------------------- | ------- |
| CAP-30 | `Selector "#missing" matched no elements.` | `tests/test_inspect_element.py:315`; `is_error is True` at `:309` | ✅ |
| CAP-31 | `Selector ".dup" matched 2 elements; it must match exactly one.` | `tests/test_inspect_element.py:320` | ✅ |
| CAP-32 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `tests/test_inspect_element.py:334` | ✅ |
| CAP-33 | `Could not load ` + URL | `tests/test_inspect_element.py:339` | ✅ |
| CAP-34 | `Could not launch Chromium` and `playwright install chromium` | `tests/test_inspect_element.py:346`, `:347` | ✅ |
| CAP-35 | `Timed out after Ns` (30 by default), within 2s of the timeout; next call answered | `tests/test_inspect_element.py:368` - `"Timed out after 1s" in text`; `:369` - `elapsed < 3`; `:370` - next call `["box"]["w"] == 120`; default at `src/squint_mcp/config.py:8` | ❌ latency gap closed (R3 killed); the message format is checked only for an integer, while the config holds `30.0` (N11 survives) |
| CAP-36 | error names `selector` | `tests/test_inspect_element.py:208`, `:209` | ✅ |
| CAP-37 | error names the offending field | `tests/test_inspect_element.py:218`, `:219`, for `width` and `height` (`:213`) | ✅ |
| CAP-38 | `Invalid selector "div[".` | `tests/test_inspect_element.py:324` | ✅ |
| CAP-39 | `Selector "#hidden" matched an element with no rendered box.` | `tests/test_inspect_element.py:329` | ✅ |

### P2: Tooling, configuration and documents (file evidence)

| ID | Evidence | How | Verdict |
| -- | -------- | --- | ------- |
| CAP-40 | `src/squint_mcp/config.py:4` and `:5` (1440×900), `:8` (30s), `:11` (3s), `:15` (16px), `:18` (512px), `:22` (3), `:27` (20 properties); source comments at `:3`, `:7`, `:10`, `:13`, `:17`, `:20`, `:24` | read | ✅ |
| CAP-41 | `pyproject.toml:10` (`pillow`), `pyproject.toml:11` (`playwright`); no `numpy` or `coloraide` in `pyproject.toml` or `uv.lock` | read + ran grep | ✅ |
| CAP-42 | imports of `playwright` under `src/` only at `src/squint_mcp/capture.py:12`, `:13`, `:14` | ran grep | ✅ |
| CAP-43 | `src/squint_mcp/js/stabilize.js:3`, `src/squint_mcp/js/collect_elements.js:3`, loaded at `src/squint_mcp/capture.py:20` and `:21`; `git grep` for `=>`, `function (`, `document.`, `window.` in `src/**/*.py`: no match | ran grep | ✅ |
| CAP-44 | `.github/workflows/ci.yml:16` (`uv run playwright install --with-deps chromium`) before `.github/workflows/ci.yml:24` (tests) | read | ✅ file verified; live CI run needs a push |
| CAP-45 | `CHANGELOG.md:13`, under `## [Unreleased]` at `CHANGELOG.md:7` | read | ✅ |
| CAP-46 | `CONTRIBUTING.md:9`; `README.md:49`, inside `## Development` (`README.md:47`): "installed once with `uv run playwright install chromium`" | read | ✅ (iteration-1 gap closed) |
| CAP-47 | `docs/ROADMAP.md:17` and `docs/ROADMAP.md:57` read `pendente` | read | ⏳ pending closing step (conditional on PASS; not a failure) |

**Status**: ❌ Gaps present. 44 of 47 criteria have evidence that matches the spec outcome and discriminates; CAP-21 and CAP-35 have a matching assertion that a contradicting mutant also passes; CAP-47 is pending by design. No ⚠️ spec-precision gap on a criterion as written; three flagged on outcomes the spec leaves undefined (see the sensor).

**Other checks**: `tests/test_ping.py:34` replaces the old "only tool" test with the exact two-tool assertion, as the spec authorises. The `monkeypatch` of `config.TOTAL_TIMEOUT_S` (`tests/test_inspect_element.py:364`) is the only reach past the MCP boundary, also authorised.

### Spec edits since iteration 1 (`git diff 4f92813..HEAD -- spec.md`, ran)

Seven criteria changed. Every edit adds an obligation or an input; none removes or loosens one. None is goalpost-moving.

| Criterion | Edit | Judgment |
| --------- | ---- | -------- |
| CAP-13 | adds "showing the page background in the margin, the blue border and the red fill" | Legitimate: the content that "the border box plus 16px on each side" already implied for this fixture |
| CAP-16 | adds `#screen` `box.h == 900` | Legitimate: gives the height half of the default viewport an outcome |
| CAP-17 | adds `#screen` `box.h == 844` | Legitimate: closes the precision gap of iteration 1. The sentence lost its "and" (`spec.md:110`), cosmetic |
| CAP-20 | adds "whether or not the page is scrolled" | Legitimate: "page coordinates" (`spec.md:49`) already implied it |
| CAP-22 | adds "including a page that goes idle only after 5 seconds" | Legitimate: one more input inside the same condition |
| CAP-35 | adds "no later than 2 seconds after the timeout elapses" | Legitimate tightening. The 2s tolerance is a new number, and it is not logged in the Assumptions table |
| CAP-46 | "development" → "Development" | Legitimate: the README was changed to comply, not the criterion relaxed |

---

## Discrimination Sensor

Scratch: a detached `git worktree` at `C:\tmp\sq-cap2` (HEAD `80577bf`), own `.venv` via `uv sync --locked`, baseline `50 passed` there. A script outside the repo applied one single-line mutant at a time (it refuses to run outside a linked worktree), ran the full `uv run pytest -q` and restored the original bytes. No `git stash`. Line numbers refer to the unmutated files.

| # | File:line | Mutation | Killed? | Killing test / note |
| - | --------- | -------- | ------- | ------------------- |
| R1 | `src/squint_mcp/vision.py:41` | crop replaced by a blank image of the right size (iteration-1 M07) | ✅ Killed | `test_crop_shows_the_element_as_painted` |
| R2 | `src/squint_mcp/js/collect_elements.js:19` | `box.y` without `window.scrollY` (M27) | ✅ Killed | `test_box_stays_in_page_coordinates_when_the_page_is_scrolled` |
| R3 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at 8x, message unchanged (M25) | ✅ Killed | `test_call_that_outlives_the_total_timeout_is_an_error_and_server_recovers` |
| R4 | `src/squint_mcp/config.py:11` | network-idle timeout 3s → 8s (M23) | ✅ Killed | `test_a_page_idle_only_after_five_seconds_is_returned_unstabilized` |
| R5 | `src/squint_mcp/capture.py:85` | browser viewport height pinned to 900 (M34) | ✅ Killed | `test_viewport_argument_sets_the_page_size` |
| N1 | `src/squint_mcp/js/collect_elements.js:18` | `box.x` without `window.scrollX` | ➖ Survived, spec-precision gap | no criterion gives an outcome under horizontal scroll |
| N2 | `src/squint_mcp/vision.py:41` | crop blanked to the right of x=77 and below y=52 | ➖ Survived, not blocking | the three regions CAP-13 names are each asserted; nothing is asserted in the far half of the crop |
| N3 | `src/squint_mcp/vision.py:41` | JPEG bytes sent as `image/png` | ✅ Killed | `test_crop_shows_the_element_as_painted` (by pixel exactness) |
| N4 | `src/squint_mcp/tools/inspect_element.py:83` | image block typed `image/jpeg` | ✅ Killed | `test_success_carries_a_summary_and_one_png_crop` |
| N5 | `src/squint_mcp/tools/inspect_element.py:79` | summary without the selector | ✅ Killed | same |
| N6 | `src/squint_mcp/models.py:12` | `height` accepts 0 | ✅ Killed | `test_viewport_smaller_than_one_pixel_is_rejected` |
| N7 | `src/squint_mcp/vision.py:27` | crop margin not clamped at the left edge | ➖ Survived, spec-precision gap | CAP-14 covers the top-right corner only |
| N8 | `src/squint_mcp/vision.py:30` | crop margin not clamped at the bottom edge | ➖ Survived, spec-precision gap | same |
| N9 | `src/squint_mcp/config.py:11` | network-idle timeout 3s → 1s | ❌ Survived | none: 50 passed. Contradicts CAP-21 |
| N10 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at half the configured value | ➖ Survived, spec-precision gap | CAP-35 bounds the error from above only |
| N11 | `src/squint_mcp/tools/inspect_element.py:54` | message format `:g` removed (`30.0s` by default) | ❌ Survived | none: 50 passed. Contradicts CAP-35 |
| N12 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at 2x | ➖ Survived, not blocking | at the tested 1s it answers at 2s, inside the criterion's own 2s tolerance |

Not repeated, known non-blocking by design: context never closed (CAP-29) and Chromium relaunched per call (CAP-28), both file-evidence criteria.

### The two blocking survivors

- **N9, CAP-21.** "WHEN the page reaches network idle within 3 seconds THEN `stabilized: true`." The only stabilized fixture (`box.html` over `file://`) is idle at once, so the bound is pinned from above (R4) and not from below. Probe in the scratch (ran): a page polling `/tick` for 1.5s returns `stabilized: true` on the real code and `false` on the mutant. The product is correct; the test cannot tell.
- **N11, CAP-35.** The spec gives the message as `Timed out after Ns` with 30 by default. `tests/test_inspect_element.py:364` patches the timeout with the integer `1`, but `src/squint_mcp/config.py:8` holds the float `30.0`; without `:g` the default message becomes `Timed out after 30.0s` and the test still sees `1s`. Probe (ran): with the timeout patched to `1.0` the real code answers `Timed out after 1s.` after 1.02s.

### Survivors that do not block

- **N1, N7, N8.** The Assumptions table says "page coordinates" (`spec.md:49`) and "clamped to the page" (`spec.md:53`), but the criteria give an outcome for vertical scroll only (CAP-20) and for the top-right corner only (CAP-14). Same kind of gap as CAP-17 in iteration 1.
- **N10, N12.** CAP-35 says "no later than 2 seconds after". It sets no lower bound, and an absolute 2s tolerance checked at a 1s timeout cannot catch a multiplier under 3x. An `elapsed >= 1` assertion closes N10 for free.
- **N2.** Contrived; listed so the reader knows the crop is checked at four points in its top-left half.

**Sensor depth**: P0-full by hand (17 behaviour-level mutations: the 5 of iteration 1 re-injected, 12 new)
**Sensor outcome**: 17 injected, 9 killed, 8 survived; 2 survivors contradict a spec criterion - FAIL ❌

**Isolation check (ran)**: real-tree `git status --porcelain` was empty before the sensor and empty after `git worktree remove --force C:/tmp/sq-cap2` (`diff` of the two captures is empty). HEAD is `80577bf` before and after, `git diff --stat HEAD` is empty, `git worktree list` shows only the main tree, `C:\tmp\sq-cap2` no longer exists.

**Flakiness check (ran)**: the two timing tests (`elapsed < 3`, idle after 5s) passed 3 of 3 extra runs in the scratch.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ |
| No scope creep | ✅ |
| Matches patterns | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ⚠️ values match; two assertions do not discriminate (CAP-21, CAP-35) |
| Per-layer Coverage Expectation met (happy, edge and error paths through the one seam) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam), ADR-0002 (only `capture.py` imports playwright) | ✅ |

---

## Edge Cases

- [x] CAP-38 invalid selector: `tests/test_inspect_element.py:324`.
- [x] CAP-39 element with no rendered box: `tests/test_inspect_element.py:329`.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest -q`
- **Outcome (ran, real tree)**: pyright exit 0 (0 errors, 0 warnings, 0 informations); ruff check exit 0 (`All checks passed!`); ruff format --check exit 0 (41 files already formatted); pytest exit 0 with 50 passed, 0 failed, 0 skipped in 29.54s
- **Test count before feature**: 12 (`main`)
- **Test count after feature**: 50 (12 in `tests/test_ping.py`, 38 in `tests/test_inspect_element.py`)
- **Delta**: +38 (+3 since iteration 1); one test renamed and re-asserted as authorised, none deleted, no assertion weakened
- **Skipped tests**: none
- **Failures**: none

---

## Fix Plans

### Fix 1: Pin the 3s network-idle bound from below (CAP-21, N9)

- **Root cause**: the only page asserted `stabilized: true` is idle at once (`tests/test_inspect_element.py:168`).
- **Fix task**: add a fixture that polls `/tick` for about 1.5s and then stops; assert `stabilized is True` over `http://`. If the criterion is to name the input, add "including a page that goes idle after about 2 seconds" to CAP-21, as was done for CAP-22. Done when N9 fails the suite. Costs about 2s of run time.
- **Priority**: Major

### Fix 2: Patch the timeout with the type the config holds (CAP-35, N11)

- **Root cause**: `tests/test_inspect_element.py:364` patches `TOTAL_TIMEOUT_S` with `1`; the config value is a float.
- **Fix task**: patch with `1.0` and keep the assertion `"Timed out after 1s" in text`. Also assert `elapsed >= 1` (closes N10). Done when N11 fails the suite.
- **Priority**: Major

### Optional, not required

- N1: a criterion and a test for `box.x` on a horizontally scrolled page.
- N7, N8: a crop-size outcome for an element at the left edge (`#full`) and at the bottom of the page (`#below`: 132×66).
- CAP-35: log the 2s tolerance in the Assumptions table.
- CAP-17: restore the missing "and" at `spec.md:110`.

---

## Requirement Traceability Update

Not applied to `spec.md` (the Verifier writes only this report). Proposed statuses:

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| CAP-01 to CAP-20, CAP-22 to CAP-34, CAP-36 to CAP-46 | Implementing | ✅ Verified |
| CAP-21, CAP-35 | Implementing | ❌ Needs a stronger test (behaviour correct) |
| CAP-47 | Pending | Pending (closing step after PASS) |

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 44/47 ACs have matching, discriminating evidence; CAP-21 and CAP-35 need a stronger test; CAP-47 pending by design
**Sensor**: 9/17 mutations killed; all 5 of iteration 1 killed; 2 blocking survivors (N9, N11), 6 non-blocking
**Gate**: 50 passed, 0 failed; pyright, ruff check, ruff format all exit 0

**What works**: everything iteration 1 listed, plus crop content, page coordinates under vertical scroll, viewport height, the upper side of the 3s idle bound, timeout latency, and the README section.

**Issues found**: two test-only fixes (Fix 1, Fix 2). No defect in the product code.

**Next steps**: apply Fix 1 and Fix 2, run iteration 3 (the last), then mark slice 2 `concluída` in `docs/ROADMAP.md` (CAP-47).
