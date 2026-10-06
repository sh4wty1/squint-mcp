# Capture + inspect_element Validation

## Validation: capture-inspect-element - PASS ✅

**Date**: 2026-10-06
**Spec**: `.specs/features/capture-inspect-element/spec.md`
**Diff range**: `main..HEAD` on `feat/capture-inspect-element` (16 commits, HEAD `92f2ea8`)
**Verifier**: independent sub-agent (author ≠ verifier), iteration 3 of at most 3

**History**: iteration 1 returned a failing verdict (four blocking mutants, CAP-46 unmet). Iteration 2 returned a failing verdict on test strength only (two blocking mutants: a 1s network-idle bound, CAP-21; a timeout message printed as `30.0s`, CAP-35). This is iteration 3. Commit `074e839` closed both, plus the left and bottom crop clamps and the half-value timeout. No product defect was found in any iteration.

All five survivors of iteration 2 that were re-injected are now killed. Fifteen further mutants were tried; nine were killed. Six survived, and none of them breaks an outcome that a criterion defines for an input the spec names. Two of the six deserve the reader's attention before merge and are ranked under "Open gaps": the downscale of a tall crop (Y9) and a timeout enforced at up to 2.9 times its value (Y11, Y15). Both are rulings of judgment, explained where they are listed.

How each claim was checked is marked **ran** (executed, output read) or **read** (file evidence only). Line numbers are from the files at `92f2ea8`. `T` = `tests/test_inspect_element.py`.

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
| T8 Documents | ✅ Done | - |
| Iteration-1 and iteration-2 fixes | ✅ Done | `85ed203`, `cbf5164`, `074e839` |

`tasks.md` has 35 ticked boxes and 0 unticked (ran grep).

---

## Spec-Anchored Acceptance Criteria

Every test row was executed in the full suite (51 passed, three runs).

### P1: Inspect one element

| ID | Spec-defined outcome | `file:line` + assertion | Verdict |
| -- | -------------------- | ----------------------- | ------- |
| CAP-01 | exactly two tools, `ping` and `inspect_element` | `tests/test_ping.py:36` - `assert sorted(tool.name for tool in tools) == ["inspect_element", "ping"]` | ✅ |
| CAP-02 | `readOnlyHint: true`, `openWorldHint: true` | `tests/test_inspect_element.py:87` - `annotations.read_only_hint is True`; `tests/test_inspect_element.py:88` - `annotations.open_world_hint is True` | ✅ |
| CAP-03 | properties exactly `url`, `selector`, `viewport`; first two string and required; `viewport` object or null | `tests/test_inspect_element.py:96` - `set(properties) == {"url", "selector", "viewport"}`; `:97`, `:98` - `["type"] == "string"`; `:99` - `set(schema["required"]) == {"url", "selector"}`; `:106` - viewport types `== {"object", "null"}` | ✅ |
| CAP-04 | keys exactly the six documented | `tests/test_inspect_element.py:233` - `assert set(content) == {...six keys...}` | ✅ |
| CAP-05 | `box == {x:40, y:60, w:120, h:70}` | `tests/test_inspect_element.py:114` - `assert content["box"] == {"x": 40, "y": 60, "w": 120, "h": 70}` | ✅ |
| CAP-06 | the exact `boxModel` literal | `tests/test_inspect_element.py:121` - `assert content["boxModel"] == {...}`, literal equal to the spec's | ✅ |
| CAP-07 | exactly the 20 properties | `tests/test_inspect_element.py:131` - `set(content["computed"]) == COMPUTED_PROPERTIES` (`:23-44`, held in the test independently of `config`; compared with `spec.md:48`, 20 names, same set) | ✅ |
| CAP-08 | `20px`, `rgb(255, 0, 0)`, `block` | `tests/test_inspect_element.py:136`, `:137`, `:138` | ✅ |
| CAP-09 | `[{#ff0000, 0.7857}, {#0000ff, 0.2143}]` | `tests/test_inspect_element.py:245` - same literal | ✅ |
| CAP-10 | exactly 3 entries, share descending | `tests/test_inspect_element.py:253` - exact list of three, shares 0.4, 0.3, 0.2 (stronger than the spec) | ✅ |
| CAP-11 | computed white, first sampled `#000000` | `tests/test_inspect_element.py:264`, `:265` | ✅ |
| CAP-12 | `isError: false`, a text block with the selector, exactly one `image/png` | `tests/test_inspect_element.py:270`, `:271`, `:273` - `[image.mime_type for image in images] == ["image/png"]` | ✅ |
| CAP-13 | crop 152×102, 1:1, showing page background, blue border, red fill | `tests/test_inspect_element.py:279` - `crop_size(...) == (152, 102)`; `:284` - `getpixel((0, 0)) == (255, 255, 255)`; `:285` - `getpixel((16, 16)) == (0, 0, 255)`; `:286` - `getpixel((21, 21)) == (255, 0, 0)`; `:287` - centre red | ✅ |
| CAP-14 | `#corner` crop 66×66; `#below` crop 116×66 | `tests/test_inspect_element.py:291` - `crop_size(client, "#corner") == (66, 66)`; `tests/test_inspect_element.py:292` - `crop_size(client, "#below") == (116, 66)`; fixture `tests/fixtures/box.html:69-76` (top 2000, left 0, 100×50) | ✅ all four edges now pinned (S3, S4, Y2 killed; right edge killed in iteration 1) |
| CAP-15 | crop 512×65 | `tests/test_inspect_element.py:296` - `== (512, 65)` | ✅ for the input the criterion names; see Y9 |
| CAP-16 | viewport 1440×900, `#full` `box.w == 1440`, `#screen` `box.h == 900` | `tests/test_inspect_element.py:143`, `:144`, `:145` | ✅ |
| CAP-17 | viewport echoed, `#full` `box.w == 390`, `#screen` `box.h == 844` | `tests/test_inspect_element.py:151`, `:152`, `:154` | ✅ |
| CAP-18 | `null` equals omission | `tests/test_inspect_element.py:159` - `inspect(..., viewport=None) == omitted` | ✅ |
| CAP-19 | shadow-root element, `color == rgb(0, 0, 255)` | `tests/test_inspect_element.py:164` | ✅ |
| CAP-20 | `box.y == 2000`, first sampled `#008000`, scrolled or not | `tests/test_inspect_element.py:301`, `:302` (unscrolled); `:310`, `:311` (`box.html#below`) | ✅ |

### P1: Stabilized, isolated Capture

| ID | Spec-defined outcome | Evidence | How | Verdict |
| -- | -------------------- | -------- | --- | ------- |
| CAP-21 | `stabilized: true` when idle within 3s, including a page busy for 1.5s first | `tests/test_inspect_element.py:168` - `["stabilized"] is True` (idle at once); `tests/test_inspect_element.py:189` - `["stabilized"] is True` for `polling-briefly.html?ms=1500` | ran | ✅ iteration-2 gap closed (S1 killed) |
| CAP-22 | `isError: false`, `stabilized: false` when not idle within 3s, including idle only after 5s | `tests/test_inspect_element.py:175` (never idle), `:182` (`?ms=5000`) - `is False`; `:68` - `result.is_error is False` | ran | ✅ |
| CAP-23 | `opacity == "1"` for animated and transitioned | `tests/test_inspect_element.py:195`, `:196-198` | ran | ✅ |
| CAP-24 | `document.fonts.ready` after `load`, before zeroing | `src/squint_mcp/capture.py:93` (`wait_until="load"`), `src/squint_mcp/capture.py:96` (script evaluated after it), `src/squint_mcp/js/stabilize.js:4` (`await document.fonts.ready`) ahead of `src/squint_mcp/js/stabilize.js:7-12` (style) and `:16-22` (finish) | read | ✅ |
| CAP-25 | http, https, file accepted | `file://`: `tests/test_inspect_element.py:114`; `http://`: `tests/test_inspect_element.py:203`; `https`: `src/squint_mcp/capture.py:79` (`scheme not in ("http", "https", "file")`) | ran + read | ✅ |
| CAP-26 | both calls report `rgb(0, 128, 0)` | `tests/test_inspect_element.py:210`, inside `for _ in range(2)` (`:208`); the fixture turns red on a second visit and blue if storage fails (`tests/fixtures/visit.html:10-19`) | ran | ✅ |
| CAP-27 | tools listed and `ping` answers without Chromium | `tests/test_inspect_element.py:362`, `:364`; fixture `tests/conftest.py:35` | ran | ✅ |
| CAP-28 | Chromium launched at most once | `src/squint_mcp/capture.py:34` (lock), `src/squint_mcp/capture.py:35` (`if self._browser is None`), `src/squint_mcp/capture.py:40` (launch), `src/squint_mcp/server.py:11` (one lifespan) | read | ✅ |
| CAP-29 | context closed on every exit path | `src/squint_mcp/capture.py:88` `try` … `src/squint_mcp/capture.py:115-116` `finally: await context.close()`; the timeout cancels once, so the `finally` runs (`src/squint_mcp/tools/inspect_element.py:49`) | read | ✅ |

### P1: Clear errors

| ID | Spec-defined text | `file:line` + assertion | Verdict |
| -- | ----------------- | ----------------------- | ------- |
| CAP-30 | `Selector "#missing" matched no elements.` | `tests/test_inspect_element.py:323`; `is_error is True` at `:317` | ✅ |
| CAP-31 | `Selector ".dup" matched 2 elements; it must match exactly one.` | `tests/test_inspect_element.py:328` | ✅ |
| CAP-32 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `tests/test_inspect_element.py:342` | ✅ |
| CAP-33 | `Could not load ` + URL | `tests/test_inspect_element.py:347` | ✅ |
| CAP-34 | `Could not launch Chromium` and `playwright install chromium` | `tests/test_inspect_element.py:354`, `:355` | ✅ |
| CAP-35 | `Timed out after Ns` with no trailing `.0`; no earlier than the timeout, no later than 2s after; next call answered | `tests/test_inspect_element.py:372` - timeout patched with the float `1.0`; `:376` - `"Timed out after 1s" in text`; `:377` - `1 <= elapsed < 3`; `:378` - next call `["box"]["w"] == 120`; default `30.0` at `src/squint_mcp/config.py:8`, format `:g` at `src/squint_mcp/tools/inspect_element.py:54` | ✅ iteration-2 gap closed (S2, S5 killed). ⚠️ the spec's 2s tolerance at a 1s test timeout admits a multiplier under 3 (Y11, Y15) |
| CAP-36 | error names `selector` | `tests/test_inspect_element.py:215`, `:216` | ✅ |
| CAP-37 | error names the offending field | `tests/test_inspect_element.py:225`, `:226`, for `width` and `height` (`:220`) | ✅ |
| CAP-38 | `Invalid selector "div[".` | `tests/test_inspect_element.py:332` | ✅ |
| CAP-39 | `Selector "#hidden" matched an element with no rendered box.` | `tests/test_inspect_element.py:337` | ✅ |

### P2: Tooling, configuration and documents (file evidence)

| ID | Evidence | How | Verdict |
| -- | -------- | --- | ------- |
| CAP-40 | `src/squint_mcp/config.py:4` and `:5` (1440×900), `:8` (30s), `:11` (3s), `:15` (16px), `:18` (512px), `:22` (3), `:27-48` (20 properties); source comments at `:3`, `:7`, `:10`, `:13`, `:17`, `:20`, `:24` | read | ✅ |
| CAP-41 | `pyproject.toml:10` (`pillow`), `pyproject.toml:11` (`playwright`); no `numpy` or `coloraide` in `pyproject.toml` or as a package in `uv.lock` | ran grep | ✅ |
| CAP-42 | imports of `playwright` under `src/` only at `src/squint_mcp/capture.py:12`, `:13`, `:14` | ran grep | ✅ |
| CAP-43 | `src/squint_mcp/js/stabilize.js:3`, `src/squint_mcp/js/collect_elements.js:3`, loaded at `src/squint_mcp/capture.py:20` and `:21`; grep for `=>`, `function (`, `document.`, `window.` in `src/**/*.py`: no match | ran grep | ✅ |
| CAP-44 | `.github/workflows/ci.yml:16` (`uv run playwright install --with-deps chromium`) before `.github/workflows/ci.yml:24` (`uv run pytest`) | read | ✅ file verified; the live CI run needs a push |
| CAP-45 | `CHANGELOG.md:13`, under `## [Unreleased]` at `CHANGELOG.md:7` | read | ✅ |
| CAP-46 | `CONTRIBUTING.md:9`; `README.md:49`, inside `## Development` (`README.md:47`) | read | ✅ |
| CAP-47 | `docs/ROADMAP.md:17` and `docs/ROADMAP.md:57` still read `pendente` | read | ⏳ pending closing step (conditional on this report; not a failure) |

**Status**: ✅ 46 of 47 criteria have evidence that matches the spec outcome; CAP-47 is the closing step this report unlocks. ⚠️ Two spec-precision gaps flagged (CAP-15 tall axis, CAP-35 tolerance), neither on an outcome a criterion defines.

**Other checks (read)**: `tests/test_ping.py:34-36` replaces the old "only tool" test with the exact two-tool assertion, as the spec authorises (`spec.md:45`). The `monkeypatch` of `config.TOTAL_TIMEOUT_S` (`tests/test_inspect_element.py:372`) is the only reach past the MCP boundary, also authorised (`spec.md:63`). No test is skipped or marked expected-to-fail.

### Spec edits since iteration 2 (`git diff 80577bf..HEAD -- spec.md`, ran)

Five edits. Each adds an obligation, names an input, or fixes punctuation. None removes or loosens an outcome. None is goalpost-moving.

| Where | Edit | Judgment |
| ----- | ---- | -------- |
| CAP-14 | adds "the crop of `#below` (100×50, in the bottom-left corner of the page) SHALL be 116×66 px" | Legitimate: a second outcome, for the two edges the first one did not reach. The fixture moved `#below` from `left: 40px` to `left: 0` to make it a corner; nothing asserted its x before, and CAP-20 still holds on it |
| CAP-17 | restores the comma lost in iteration 1's edit | Cosmetic |
| CAP-21 | adds "including a page that stays busy for 1.5 seconds first" | Legitimate: one more input inside the same condition, as was done for CAP-22 |
| CAP-35 | adds "written without a trailing `.0` (`Timed out after 30s` by default)" and "no earlier than the timeout" | Legitimate: both tighten. The first states what the message example already showed; the second adds a lower bound that was missing |
| Assumptions, "Timeout latency" | logs the 2s tolerance and its reason | Legitimate: iteration 2 asked for this number to be recorded. The number itself is what lets Y11 and Y15 through; see "Open gaps" |

---

## Discrimination Sensor

Scratch: a detached `git worktree` at `C:\tmp\sq-cap3` (HEAD `92f2ea8`), its own `.venv` via `uv sync --locked`, baseline `51 passed` there. A script kept outside the repo applied one single-line mutant at a time (it refuses to run unless the target is a linked worktree), ran the full `uv run pytest -q` and wrote the original bytes back. No `git stash`. Line numbers refer to the unmutated files.

| # | File:line | Mutation | Killed? | Killing test / note |
| - | --------- | -------- | ------- | ------------------- |
| S1 | `src/squint_mcp/config.py:11` | network-idle timeout 3s → 1s (iteration-2 N9) | ✅ Killed | `test_a_page_idle_after_a_second_and_a_half_is_stabilized` |
| S2 | `src/squint_mcp/tools/inspect_element.py:54` | timeout message without `:g` (N11) | ✅ Killed | `test_call_that_outlives_the_total_timeout_is_an_error_and_server_recovers` |
| S3 | `src/squint_mcp/vision.py:27` | crop margin not clamped at the left edge (N7) | ✅ Killed | `test_crop_margin_is_clamped_to_the_page` |
| S4 | `src/squint_mcp/vision.py:30` | crop margin not clamped at the bottom edge (N8) | ✅ Killed | same |
| S5 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at half the configured value (N10) | ✅ Killed | timeout test (`1 <= elapsed`) |
| Y1 | `src/squint_mcp/capture.py:99` | network-idle wait of 2.4s instead of 3s | ➖ Survived, not blocking | inside the band between the two inputs the spec names |
| Y2 | `src/squint_mcp/vision.py:28` | crop margin not clamped at the top edge alone | ✅ Killed | `test_crop_margin_is_clamped_to_the_page` |
| Y3 | `src/squint_mcp/models.py:11` | `width` accepts 0 | ✅ Killed | `test_viewport_smaller_than_one_pixel_is_rejected` |
| Y4 | `src/squint_mcp/js/collect_elements.js:20` | `box.w` from `clientWidth` (padding box) | ✅ Killed | six tests, first `test_box_is_the_border_box_in_page_coordinates` |
| Y5 | `src/squint_mcp/js/collect_elements.js:33` | `computed` read from the inline style | ✅ Killed | `test_computed_values_are_what_the_browser_resolved` and two more |
| Y6 | `src/squint_mcp/vision.py:62` | hex in upper case | ✅ Killed | both sampled-colour list tests |
| Y7 | `src/squint_mcp/tools/inspect_element.py:85` | structured content without camelCase aliases | ✅ Killed | most of the suite |
| Y8 | `src/squint_mcp/capture.py:90` | Playwright's own 30s default timeout left on | ➖ Survived, not blocking | no criterion; differs only in a race at the 30s mark |
| Y9 | `src/squint_mcp/vision.py:39` | downscale limits the width only, a tall crop is not reduced | ➖ Survived, spec-precision gap | CAP-15 gives an outcome for a wide element only |
| Y10 | `src/squint_mcp/server.py:19` | `open_world_hint` false | ✅ Killed | `test_inspect_element_is_read_only_and_open_world` |
| Y11 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at 2x (iteration-2 N12, ruled again) | ➖ Survived, spec-precision gap | at the tested 1s it answers at 2s, inside the spec's own 2s tolerance |
| Y12 | `src/squint_mcp/capture.py:93` | navigation waits for `domcontentloaded`, not `load` | ➖ Survived by design | CAP-24 is a file-evidence criterion |
| Y13 | `src/squint_mcp/vision.py:39` | downscale limits the height only | ✅ Killed | `test_crop_is_downscaled_to_512px_on_its_longest_side` |
| Y14 | `src/squint_mcp/capture.py:102` | the idle wait swallows any Playwright error, not only a timeout | ➖ Survived, not blocking | no criterion describes a non-timeout failure of that wait |
| Y15 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at 2.9x | ➖ Survived, spec-precision gap | same as Y11: it answers at about 2.9s, under the 3s bound |

Not repeated, known non-blocking by design: context never closed (CAP-29), Chromium relaunched per call (CAP-28), `box.x` without `window.scrollX`, one of the two animation-zeroing halves removed.

### Why no survivor blocks

A survivor blocks when the suite misses an outcome that a criterion defines for an input the spec names. Iteration 2's two blockers were of that kind and could be closed without leaving the spec. None of these six is.

- **Y11, Y15 (CAP-35).** The spec fixes both the test method (timeout lowered to 1, `spec.md:63`) and the tolerance (2 seconds, `spec.md:64` and CAP-35). The test asserts exactly that: `1 <= elapsed < 3` (`tests/test_inspect_element.py:377`). Under those two numbers any multiplier below 3 complies with the criterion at the tested value, while at the default 30s a 2x timeout would answer at 60s, well past the 32s the criterion allows. The weakness is in the spec's choice of tolerance, not in a test weaker than the spec: closing it needs a tolerance tighter than the spec grants, or a test timeout the spec does not prescribe. The Assumptions row's own reason ("a looser bound would hide a timeout enforced at the wrong value") shows the intent is not fully met. This is the closest call in the report.
- **Y9 (CAP-15).** CAP-15 names `#wide` and 512×65, and the test asserts it. The rule "512px on the longest side" lives in the Assumptions table (`spec.md:54`) and the Success Criteria (`spec.md:252`), neither of which is one of the 47 criteria. Same shape as the clamp edges that iteration 2 listed as non-blocking and that CAP-14 has since absorbed. Y13 shows the wide axis is pinned.
- **Y1 (CAP-21, CAP-22).** The criteria name their inputs: busy for 1.5s (idle at about 2s) and idle after 5s. Both are asserted. A bound anywhere between about 2.1s and 5.5s passes both. The value itself is pinned by file evidence: `src/squint_mcp/config.py:11` holds 3.0 (CAP-40) and `src/squint_mcp/capture.py:99` uses it unscaled. A tighter behavioural bracket would trade this for a timing-sensitive test.
- **Y12.** The spec assigns CAP-24 to file evidence (`spec.md:67`); the fixtures have no subresources, so the two load events coincide.
- **Y8, Y14.** No criterion speaks to them.

**Sensor depth**: P0-full by hand (20 behaviour-level mutations: 5 survivors of iteration 2 re-injected, 15 new or re-ruled)
**Sensor outcome**: 20 injected, 13 killed, 7 survived; 0 survivors contradict an outcome a criterion defines for a spec-named input - PASS ✅

**Isolation check (ran)**: real-tree `git status --porcelain` was empty (0 bytes) before the sensor and empty after `git worktree remove --force C:/tmp/sq-cap3`; `diff` of the two captures is empty. HEAD is `92f2ea8` before and after, `git diff --stat HEAD` is empty, `git worktree list` shows only the main tree, `C:\tmp\sq-cap3` no longer exists. The scratch itself was clean (`git status --porcelain` empty) after the last mutant.

**Flakiness check (ran)**: the full suite passed 3 of 3 runs in the real tree and once more as the scratch baseline. In the 7 surviving-mutant runs all 51 tests passed, and in the 13 killed runs every failing test is explained by the mutant. No unrelated failure in 24 runs.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ |
| No scope creep | ✅ |
| Matches patterns | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met (happy, edge and error paths through the one seam) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam), ADR-0002 (only `capture.py` imports playwright) | ✅ |

---

## Edge Cases

- [x] CAP-38 invalid selector: `tests/test_inspect_element.py:332`.
- [x] CAP-39 element with no rendered box: `tests/test_inspect_element.py:337`.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest -q`
- **Outcome (ran, real tree)**: pyright exit 0 (0 errors, 0 warnings, 0 informations); ruff check exit 0 (`All checks passed!`); ruff format --check exit 0 (41 files already formatted); pytest exit 0 three times: 51 passed in 32.44s, 51 passed in 32.69s, 51 passed in 32.36s
- **Test count before feature**: 12 (`main`)
- **Test count after feature**: 51 (12 in `tests/test_ping.py`, 39 in `tests/test_inspect_element.py`)
- **Delta**: +39 (+1 since iteration 2); one test renamed and re-asserted as authorised, none deleted, no assertion weakened
- **Skipped tests**: none
- **Failures**: none

---

## Open gaps (ranked, none blocking)

1. **CAP-15, Y9**: a tall crop is not shown to be reduced. `tests/test_inspect_element.py:296` asserts a wide element only. Fix: give CAP-15 a second outcome for `#screen` (1×900, crop source 17×916, so 512px high) and assert its height in the same test. One line of spec, one of test.
2. **CAP-35, Y11 and Y15**: a timeout enforced at up to 2.9 times its value passes. `tests/test_inspect_element.py:377` asserts the spec's bound exactly. Fix: tighten the tolerance in `spec.md:64` and CAP-35 to a fraction of the tested timeout (the measured overhead was about 0.02s in iteration 2; 0.5s would kill every multiplier from 1.5 up), then change the assertion to match.
3. **CAP-21 and CAP-22, Y1**: the idle bound is bracketed between about 2.1s and 5.5s. Optional; a tighter bracket costs run time and timing margin.
4. **CAP-44**: the CI file is verified; the live run needs the branch pushed.
5. **CAP-47**: mark slice 2 `concluída` at `docs/ROADMAP.md:17` and `docs/ROADMAP.md:57`.

---

## Requirement Traceability Update

Not applied to `spec.md` (the Verifier writes only this report). Proposed statuses:

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| CAP-01 to CAP-46 | Implementing | ✅ Verified |
| CAP-47 | Pending | Pending (closing step, now unlocked) |

---

## Summary

**Overall**: ✅ Ready, with two flagged spec-precision gaps

**Spec-anchored check**: 46/47 ACs matched the spec outcome; CAP-47 pending by design; 2 spec-precision gaps flagged (CAP-15 tall axis, CAP-35 tolerance)
**Sensor**: 13/20 mutations killed; all 5 of iteration 2's re-injected survivors killed; 7 survivors, none blocking
**Gate**: 51 passed, 0 failed, three runs; pyright, ruff check, ruff format all exit 0

**What works**: everything iterations 1 and 2 listed, plus the lower side of the 3s idle bound, the timeout message format with the config's own type, the lower bound on timeout latency, and the crop clamp at all four page edges.

**Issues found**: no product defect. Two places where the spec is less precise than its own Assumptions (gaps 1 and 2).

**Next steps**: mark slice 2 `concluída` in `docs/ROADMAP.md` (CAP-47); decide whether to close gaps 1 and 2 before or after merge.
