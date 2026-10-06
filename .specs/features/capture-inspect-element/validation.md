# Capture + inspect_element Validation

## Validation: capture-inspect-element - FAIL ❌

**Date**: 2026-10-06
**Spec**: `.specs/features/capture-inspect-element/spec.md`
**Diff range**: `main..HEAD` on `feat/capture-inspect-element` (11 commits, `36946ae`..`4f92813`)
**Verifier**: independent sub-agent (author ≠ verifier), iteration 1

The implementation behaves as specified on everything I could observe: all four gates are green, every testable criterion has an assertion on the spec-defined value, and two out-of-band probes of the real server returned correct data. The verdict is FAIL on test strength and one document criterion, not on a product defect:

- Four behaviour-level mutants that contradict a spec criterion pass the whole suite (M07, M23, M25, M27).
- CAP-46 is not met to the letter: the Chromium install command is not in the README's Development section.

One spec-precision gap (CAP-17, viewport height) and two redundancy survivors (M18, M19) are flagged without blocking. CAP-47 is a pending closing step, conditional on a passing verdict.

How each claim was checked is marked **ran** (executed, output read) or **read** (file evidence only). Line numbers are from the files at `4f92813`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 Dependencies | ✅ Done | commit `2f3df6a` |
| T2 Config defaults | ✅ Done | commit `e420f32` |
| T3 Capture + tool | ✅ Done | commit `6582b72` |
| T4 Crop + sampled colours | ✅ Done | commit `49f4799` |
| T5 Clear errors | ✅ Done | commit `916fb20` |
| T6 Total timeout | ✅ Done | commit `b2b0567` |
| T7 Chromium in CI | ✅ Done | commit `740b6e3` |
| T8 Documents | ⚠️ Partial | commits `6697c5c`, `4f92813`; README line is in the wrong section (CAP-46) |

`tasks.md` has 35 ticked boxes and 0 unticked (ran grep).

---

## Spec-Anchored Acceptance Criteria

All test rows below were executed in the full suite (47 passed). `T` = `tests/test_inspect_element.py`.

### P1: Inspect one element

| ID | Spec-defined outcome | `file:line` + assertion | Verdict |
| -- | -------------------- | ----------------------- | ------- |
| CAP-01 | exactly two tools, `ping` and `inspect_element` | `tests/test_ping.py:36` - `assert sorted(tool.name for tool in tools) == ["inspect_element", "ping"]` | ✅ |
| CAP-02 | `readOnlyHint: true`, `openWorldHint: true` | `tests/test_inspect_element.py:82` - `assert annotations.read_only_hint is True`; `tests/test_inspect_element.py:83` - `assert annotations.open_world_hint is True` | ✅ |
| CAP-03 | properties exactly `url`, `selector`, `viewport`; first two string and required; `viewport` object or null | `tests/test_inspect_element.py:91` - `assert set(properties) == {"url", "selector", "viewport"}`; `:92`, `:93` - `["type"] == "string"`; `:94` - `assert set(schema["required"]) == {"url", "selector"}`; `:101` - viewport types `== {"object", "null"}` | ✅ |
| CAP-04 | keys exactly the six documented | `tests/test_inspect_element.py:211` - `assert set(content) == {"viewport", "stabilized", "box", "boxModel", "computed", "sampledColors"}` | ✅ |
| CAP-05 | `box == {x:40, y:60, w:120, h:70}` | `tests/test_inspect_element.py:109` - `assert content["box"] == {"x": 40, "y": 60, "w": 120, "h": 70}` | ✅ |
| CAP-06 | the exact `boxModel` literal | `tests/test_inspect_element.py:116` - `assert content["boxModel"] == {...}`, literal equal to the spec's | ✅ |
| CAP-07 | exactly the 20 properties | `tests/test_inspect_element.py:126` - `assert set(content["computed"]) == COMPUTED_PROPERTIES` (`:22-43`, the 20 names of `spec.md:48`, held in the test independently of `config`) | ✅ |
| CAP-08 | `font-size: 20px`, `background-color: rgb(255, 0, 0)`, `display: block` | `tests/test_inspect_element.py:131`, `:132`, `:133` - three equality assertions | ✅ |
| CAP-09 | `[{#ff0000, 0.7857}, {#0000ff, 0.2143}]` | `tests/test_inspect_element.py:223` - `assert content["sampledColors"] == [...]`, same literal | ✅ |
| CAP-10 | exactly 3 entries, share descending | `tests/test_inspect_element.py:231` - exact list `#0a0a0a 0.4`, `#141414 0.3`, `#1e1e1e 0.2` (stronger than the spec) | ✅ |
| CAP-11 | computed white, first sampled `#000000` | `tests/test_inspect_element.py:242`, `:243` | ✅ |
| CAP-12 | `isError: false`, a text block with the selector, exactly one `image/png` | `tests/test_inspect_element.py:248` - `is_error is False`; `:249` - `any("#solid" in text ...)`; `:251` - `[image.mime_type for image in images] == ["image/png"]` | ✅ |
| CAP-13 | crop 152×102, the border box plus 16px each side | `tests/test_inspect_element.py:257` - `assert await crop_size(client, "#solid") == (152, 102)` | ⚠️ size only: the crop's pixels are never asserted (mutant M07 survives) |
| CAP-14 | crop 66×66 | `tests/test_inspect_element.py:261` - `== (66, 66)` | ✅ |
| CAP-15 | crop 512×65 | `tests/test_inspect_element.py:265` - `== (512, 65)` | ✅ |
| CAP-16 | viewport 1440×900, `#full` `box.w == 1440` | `tests/test_inspect_element.py:138`, `:139` | ✅ |
| CAP-17 | viewport echoed, `#full` `box.w == 390` | `tests/test_inspect_element.py:145`, `:146` | ✅ on the spec's outcome; ⚠️ Spec-precision gap: no outcome depends on `height` (mutant M34 survives) |
| CAP-18 | `null` equals omission | `tests/test_inspect_element.py:151` - `assert await inspect(client, BOX, "#full", viewport=None) == omitted` | ✅ |
| CAP-19 | shadow-root element, `color == rgb(0, 0, 255)` | `tests/test_inspect_element.py:156` | ✅ |
| CAP-20 | `box.y == 2000`, first sampled `#008000` | `tests/test_inspect_element.py:270`, `:271` | ✅ on the spec's input; page-coordinate arithmetic untested under scroll (mutant M27 survives) |

### P1: Stabilized, isolated Capture

| ID | Spec-defined outcome | Evidence | How | Verdict |
| -- | -------------------- | -------- | --- | ------- |
| CAP-21 | `stabilized: true` when idle within 3s | `tests/test_inspect_element.py:160` - `["stabilized"] is True` | ran | ✅ |
| CAP-22 | `isError: false`, `stabilized: false` when not idle within 3s | `tests/test_inspect_element.py:167` - `assert content["stabilized"] is False`; `:67` - `assert result.is_error is False` | ran | ⚠️ the 3s bound itself is not pinned (mutant M23, 8s, survives) |
| CAP-23 | `opacity == "1"` for animated and transitioned | `tests/test_inspect_element.py:173`, `:174-176` | ran | ✅ |
| CAP-24 | `document.fonts.ready` after `load`, before zeroing | `src/squint_mcp/capture.py:93` (`wait_until="load"`), `src/squint_mcp/capture.py:96` (runs stabilize.js), `src/squint_mcp/js/stabilize.js:4` (`await document.fonts.ready`) ahead of `src/squint_mcp/js/stabilize.js:7-22` | read | ✅ |
| CAP-25 | http, https, file accepted | `file://`: every fixture test, e.g. `tests/test_inspect_element.py:109`; `http://`: `tests/test_inspect_element.py:181`; `https`: `src/squint_mcp/capture.py:79` (`scheme not in ("http", "https", "file")`) | ran + read | ✅ |
| CAP-26 | both calls report `rgb(0, 128, 0)` | `tests/test_inspect_element.py:188`, inside `for _ in range(2)` (`:186`) | ran | ✅ |
| CAP-27 | tools listed and `ping` answers without Chromium | `tests/test_inspect_element.py:322` - names `== ["inspect_element", "ping"]`; `:324` - `result.is_error is False`; fixture `tests/conftest.py:35` | ran | ✅ |
| CAP-28 | Chromium launched at most once | `src/squint_mcp/capture.py:34-35` (lock, `if self._browser is None`), `src/squint_mcp/capture.py:40`, `src/squint_mcp/server.py:11` (one lifespan) | read | ✅ |
| CAP-29 | context closed on every exit path | `src/squint_mcp/capture.py:88` `try` … `src/squint_mcp/capture.py:115-116` `finally: await context.close()`; `src/squint_mcp/tools/inspect_element.py:49` uses `asyncio.timeout`, whose single cancellation lets the `finally` run | read | ✅ |

### P1: Clear errors

| ID | Spec-defined text | `file:line` + assertion | Verdict |
| -- | ----------------- | ----------------------- | ------- |
| CAP-30 | `Selector "#missing" matched no elements.` | `tests/test_inspect_element.py:283`; `is_error is True` at `:277` | ✅ |
| CAP-31 | `Selector ".dup" matched 2 elements; it must match exactly one.` | `tests/test_inspect_element.py:288` | ✅ |
| CAP-32 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `tests/test_inspect_element.py:302` | ✅ |
| CAP-33 | `Could not load ` + URL | `tests/test_inspect_element.py:307` - `assert f"Could not load {url}" in ...` | ✅ |
| CAP-34 | `Could not launch Chromium` and `playwright install chromium` | `tests/test_inspect_element.py:314`, `:315` | ✅ |
| CAP-35 | `Timed out after Ns`; next call answered | `tests/test_inspect_element.py:334` - `assert "Timed out after 1s" in text`; `:335` - next call `["box"]["w"] == 120`; default 30 at `src/squint_mcp/config.py:8` | ⚠️ elapsed time not bounded (mutant M25, 8x the limit, survives) |
| CAP-36 | error names `selector` | `tests/test_inspect_element.py:193`, `:194` | ✅ |
| CAP-37 | error names the offending field | `tests/test_inspect_element.py:203`, `:204`, for both `width` and `height` (`:198`) | ✅ |
| CAP-38 | `Invalid selector "div[".` | `tests/test_inspect_element.py:292` | ✅ |
| CAP-39 | `Selector "#hidden" matched an element with no rendered box.` | `tests/test_inspect_element.py:297` | ✅ |

### P2: Tooling, configuration and documents (file evidence)

| ID | Evidence | How | Verdict |
| -- | -------- | --- | ------- |
| CAP-40 | `src/squint_mcp/config.py:4-5` (1440×900), `:8` (30s), `:11` (3s), `:15` (16px), `:18` (512px), `:22` (3), `:27-48` (20 properties); source comments at `:3`, `:7`, `:10`, `:13`, `:17`, `:20`, `:24` | read | ✅ |
| CAP-41 | `pyproject.toml:10` (`pillow`), `pyproject.toml:11` (`playwright`); no `numpy` or `coloraide` in `pyproject.toml` or as a package in `uv.lock` | read + ran grep | ✅ |
| CAP-42 | grep for `playwright` under `src/`: imports only at `src/squint_mcp/capture.py:12-14` | ran grep | ✅ |
| CAP-43 | page code in `src/squint_mcp/js/stabilize.js:3` and `src/squint_mcp/js/collect_elements.js:3`, loaded at `src/squint_mcp/capture.py:20-21`; grep for `=>`, `function (`, `document.`, `window.` in `src/**/*.py`: no match | ran grep | ✅ |
| CAP-44 | `.github/workflows/ci.yml:15-16` (`uv run playwright install --with-deps chromium`) before `.github/workflows/ci.yml:23-24` (tests) | read | ✅ file verified; live CI run needs a push |
| CAP-45 | `CHANGELOG.md:13`, under `## [Unreleased]` at `CHANGELOG.md:7` | read | ✅ |
| CAP-46 | `CONTRIBUTING.md:9` has the command. In the README it is at `README.md:28`, inside "Run from a checkout" (`README.md:20`), commented "the browser inspect_element drives". The Development section (`README.md:47-58`) does not give it | read | ❌ GAP |
| CAP-47 | `docs/ROADMAP.md:17` and `docs/ROADMAP.md:57` read `pendente` | read | ⏳ pending closing step (conditional on a passing verdict; not a failure) |

**Status**: ❌ Gaps present. 45 of 47 criteria have evidence matching the spec outcome; CAP-46 fails; CAP-47 is pending by design. Four criteria (CAP-13, CAP-20, CAP-22, CAP-35) have a passing assertion that a contradicting mutant also passes. One spec-precision gap (CAP-17).

**Other checks**: the old `test_ping_is_the_only_tool` was replaced by the exact two-tool assertion at `tests/test_ping.py:34-36` (ran `git diff main..HEAD -- tests/test_ping.py`), as the spec authorises. The timeout test's `monkeypatch` of `config.TOTAL_TIMEOUT_S` (`tests/test_inspect_element.py:332`) is the only reach past the MCP boundary, also authorised.

**Out-of-band probes of the real server (ran, in-memory client)**: `box.html#below` returns `box.y == 2000` and `#008000` at share 1.0; the `#solid` crop has white at (0,0), blue at (16,16), red at (21,21), blue at (135,85), white at (136,86); a 390×844 call returns `#full` at `w == 390`. The product is correct where the tests are blind.

---

## Discrimination Sensor

Scratch: a detached `git worktree` at `C:\tmp\sq-cap` (HEAD `4f92813`), own `.venv` via `uv sync --locked`, baseline `47 passed` there. A script applied one mutant at a time to the worktree (it refuses to run outside a linked worktree), ran the full `uv run pytest -q`, and restored the original bytes. No `git stash`. Line numbers refer to the unmutated files.

| # | File:line | Mutation | Killed? | Killing test(s) |
| - | --------- | -------- | ------- | --------------- |
| M01 | `src/squint_mcp/capture.py:84` | one browser context reused across calls | ✅ Killed | `test_calls_do_not_share_browser_storage` |
| M02 | `src/squint_mcp/config.py:15` | crop margin 16 → 8 | ✅ Killed | three crop-size tests |
| M03 | `src/squint_mcp/vision.py:27` | margin not clamped at left/top | ✅ Killed | `test_crop_margin_is_clamped_to_the_page` |
| M04 | `src/squint_mcp/vision.py:29` | margin not clamped at the right edge | ✅ Killed | same |
| M05 | `src/squint_mcp/config.py:18` | downscale limit 512 → 600 | ✅ Killed | `test_crop_is_downscaled_to_512px_on_its_longest_side` |
| M06 | `src/squint_mcp/vision.py:39` | crop always resized to 512 (upscales) | ✅ Killed | two crop-size tests |
| M07 | `src/squint_mcp/vision.py:40` | crop pixels replaced by a blank image of the right size | ❌ Survived | none: 47 passed |
| M08 | `src/squint_mcp/vision.py:59` | sampled colours ascending | ✅ Killed | two sampled-colour tests |
| M09 | `src/squint_mcp/config.py:22` | colour limit 3 → 2 | ✅ Killed | `test_sampled_colors_keep_the_three_most_frequent` |
| M10 | `src/squint_mcp/config.py:22` | colour limit 3 → 4 | ✅ Killed | same |
| M11 | `src/squint_mcp/vision.py:62` | share rounded to 2 decimals | ✅ Killed | `test_sampled_colors_are_the_painted_colors_by_share` |
| M12 | `src/squint_mcp/vision.py:50` | colours sampled from the box plus 1px | ✅ Killed | three tests |
| M13 | `src/squint_mcp/tools/inspect_element.py:55` | zero-match check removed | ✅ Killed | `test_selector_matching_nothing_is_an_error` |
| M14 | `src/squint_mcp/tools/inspect_element.py:57` | `> 1` → `> 2` | ✅ Killed | `test_selector_matching_several_elements_is_an_error` |
| M15 | `src/squint_mcp/tools/inspect_element.py:65` | no-rendered-box check removed | ✅ Killed | `test_element_with_no_rendered_box_is_an_error` |
| M16 | `src/squint_mcp/capture.py:79` | scheme check lets `ftp` through | ✅ Killed | `test_unsupported_url_scheme_is_an_error` |
| M17 | `src/squint_mcp/capture.py:79` | scheme check rejects `http` | ✅ Killed | three HTTP tests |
| M18 | `src/squint_mcp/js/stabilize.js:12` | zero-duration style not injected | ➖ Survived, redundant on the spec's inputs | none: 47 passed |
| M19 | `src/squint_mcp/js/stabilize.js:16-22` | running animations not finished | ➖ Survived, redundant on the spec's inputs | none: 47 passed |
| M20 | `src/squint_mcp/js/stabilize.js:12,16-22` | no animation zeroing at all (M18 + M19) | ✅ Killed | `test_animations_and_transitions_are_taken_to_their_end` |
| M21 | `src/squint_mcp/capture.py:104` | `stabilized` true after a network-idle timeout | ✅ Killed | `test_a_page_that_never_goes_network_idle_is_returned_unstabilized` |
| M22 | `src/squint_mcp/capture.py:101` | `stabilized` false when idle | ✅ Killed | `test_a_page_that_goes_network_idle_is_stabilized` |
| M23 | `src/squint_mcp/config.py:11` | network-idle timeout 3s → 8s | ❌ Survived | none: 47 passed (run 5s slower) |
| M24 | `src/squint_mcp/tools/inspect_element.py:49` | total timeout removed | ✅ Killed (suite hangs; stopped at 200s) | timeout test never returns |
| M25 | `src/squint_mcp/tools/inspect_element.py:49` | timeout enforced at 8x the configured value, message unchanged | ❌ Survived | none: 47 passed (run 7s slower) |
| M26 | `src/squint_mcp/tools/inspect_element.py:54` | message always says 30s | ✅ Killed | timeout test |
| M27 | `src/squint_mcp/js/collect_elements.js:19` | `box.y` without `window.scrollY` | ❌ Survived | none: 47 passed |
| M28 | `src/squint_mcp/js/collect_elements.js:21` | `box.h` reports the width | ✅ Killed | seven tests |
| M29 | `src/squint_mcp/js/collect_elements.js:28` | `content.w` ignores right padding | ✅ Killed | `test_box_model_reports_margin_border_padding_and_content` |
| M30 | `src/squint_mcp/js/collect_elements.js:29` | `content.h` ignores bottom border | ✅ Killed | same |
| M31 | `src/squint_mcp/js/collect_elements.js:24` | `margin` reads padding | ✅ Killed | same |
| M32 | `src/squint_mcp/config.py:4` | default width 1440 → 1280 | ✅ Killed | `test_default_viewport_is_1440_by_900` |
| M33 | `src/squint_mcp/config.py:5` | default height 900 → 800 | ✅ Killed | same |
| M34 | `src/squint_mcp/capture.py:85` | browser viewport height pinned to 900, reported viewport unchanged | ➖ Survived, spec-precision gap | none: 47 passed |
| M35 | `src/squint_mcp/capture.py:85` | browser viewport width pinned to 1440 | ✅ Killed | `test_viewport_argument_sets_the_page_size` |
| M36 | `src/squint_mcp/capture.py:86` | `device_scale_factor` 1 → 2 | ✅ Killed | five tests |
| M37 | `src/squint_mcp/capture.py:114` | viewport-only screenshot | ✅ Killed | `test_an_element_below_the_fold_has_pixels` |
| M38 | `src/squint_mcp/capture.py:58` | Chromium launched eagerly in the lifespan | ✅ Killed | both missing-Chromium tests |
| M39 | `src/squint_mcp/capture.py:105` | `css:light` engine (no shadow piercing) | ✅ Killed | `test_selector_reaches_into_an_open_shadow_root` |
| M40 | `src/squint_mcp/capture.py:116` | context never closed (CAP-29) | ➖ Survived by design | file-evidence criterion |
| M41 | `src/squint_mcp/capture.py:35` | Chromium launched on every call (CAP-28) | ➖ Survived by design | file-evidence criterion |

### The four blocking survivors

- **M07, CAP-13.** The spec says the crop is "the border box plus 16px on each side". `crop_size` (`tests/test_inspect_element.py:72-76`) decodes the image and keeps only `.size`, so a crop of the right size with any content passes. The crop is half of what the tool exists to return.
- **M27, CAP-20 and the `box` assumption (`spec.md:49`, "page coordinates").** No test captures a page that is scrolled when elements are collected, so `+ window.scrollY` is never exercised. The difference is real: against the mutant, `box.html#below` returned `box.y == 850` and sampled `#ffffff` (ran); the real code returns 2000 and `#008000`.
- **M25, CAP-35.** The test proves a timeout error arrives and names the configured number, not that it arrives near that number. With the limit patched to 1s the mutant answered after 8s and passed.
- **M23, CAP-21 and CAP-22.** "Within 3 seconds" is not pinned from above: the only unstabilized fixture polls forever, so any larger bound passes.

### Survivors that do not block

- **M18, M19.** Each half of the animation zeroing covers the other on `motion.html`; removing both (M20) is killed. The inputs that tell them apart (an animation that starts after stabilization, one inside a shadow tree, an infinite one) are named in comments at `src/squint_mcp/js/stabilize.js:6` and `:14-15` but in no criterion. Out of spec; listed as optional hardening.
- **M34.** CAP-17 defines no outcome that depends on the viewport height, so the criterion as written is satisfied. Recorded as a spec-precision gap.
- **M40, M41.** CAP-29 and CAP-28 are assigned to file evidence by the spec (`spec.md:66`); the evidence is in the table above.

**Sensor depth**: P0-full by hand (41 behaviour-level mutations)
**Sensor outcome**: 41 injected, 32 killed, 9 survived; 4 survivors contradict a spec criterion - FAIL ❌

**Isolation check (ran)**: real-tree `git status --porcelain` was empty before the sensor and empty after `git worktree remove --force C:/tmp/sq-cap` (`diff` of the two captures is empty). HEAD is `4f92813` before and after, `git diff --stat HEAD` is empty, `git worktree list` shows only the main tree, and `C:\tmp\sq-cap` no longer exists. No headless Chromium process was left behind by the hung M24 run.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code (8 source files, about 420 lines; no speculative abstraction) | ✅ |
| Surgical changes (diff touches only files the tasks name) | ✅ |
| No scope creep (no Finding model, no pool, no `numpy` / `coloraide`) | ✅ |
| Matches patterns (same tool registration and test style as slice 1) | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ⚠️ values match; four assertions are too loose to discriminate |
| Per-layer Coverage Expectation met (happy, edge and error paths through the one seam) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam), ADR-0002 (only `capture.py` imports playwright) | ✅ |

---

## Edge Cases

- [x] CAP-38 invalid selector: `tests/test_inspect_element.py:292`.
- [x] CAP-39 element with no rendered box: `tests/test_inspect_element.py:297`, mutant M15 killed.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`
- **Outcome (ran, real tree)**: pyright exit 0 (0 errors, 0 warnings, 0 informations); ruff check exit 0 (`All checks passed!`); ruff format --check exit 0 (40 files already formatted); pytest exit 0 with 47 passed, 0 failed, 0 skipped in 24.07s
- **Test count before feature**: 12 (`main`)
- **Test count after feature**: 47 (12 in `tests/test_ping.py`, 35 in `tests/test_inspect_element.py`)
- **Delta**: +35; one test renamed and re-asserted as authorised (`tests/test_ping.py:34`), none deleted
- **Skipped tests**: none
- **Failures**: none

---

## Fix Plans

### Fix 1: Assert what the crop shows (CAP-13, M07)

- **Root cause**: `crop_size` discards the pixels (`tests/test_inspect_element.py:76`).
- **Fix task**: in the `#solid` crop test, also assert pixel colours at known offsets: white at (0, 0), blue at (16, 16), red at (21, 21), blue at (135, 85), white at (136, 86). Done when M07 fails the suite.
- **Priority**: Major

### Fix 2: Exercise page coordinates on a scrolled page (CAP-20, M27)

- **Root cause**: no capture happens with `window.scrollY != 0`.
- **Fix task**: add a test calling `box.html#below` with selector `#below`, asserting `box.y == 2000` and first sampled colour `#008000`. Done when M27 fails the suite.
- **Priority**: Major

### Fix 3: Bound the elapsed time of the timeout test (CAP-35, M25)

- **Root cause**: `tests/test_inspect_element.py:333-334` checks the message, not when it arrives.
- **Fix task**: measure the call with `time.monotonic()` and assert it returns in under about 3s with the limit patched to 1. Done when M25 fails the suite.
- **Priority**: Major

### Fix 4: Pin the 3s network-idle bound (CAP-21, CAP-22, M23)

- **Root cause**: the only busy fixture never goes idle.
- **Fix task**: add a fixture that polls `/tick` for about 5s and then stops; assert `stabilized is False`. Done when M23 fails the suite. Costs about 3s of run time.
- **Priority**: Minor

### Fix 5: Put the Chromium command in the README's Development section (CAP-46)

- **Root cause**: the line was added to "Run from a checkout" (`README.md:28`) only.
- **Fix task**: add `uv run playwright install chromium` to the Development section (`README.md:47-58`), or amend CAP-46 to name the section that has it.
- **Priority**: Cosmetic

### Optional, not required

- CAP-17: give the spec an outcome that depends on the viewport height (for example an element with `height: 100vh` whose `box.h` is 844), then assert it (M34).
- Animation zeroing: fixtures for an animation inside a shadow tree and for one that starts after stabilization would separate M18 from M19.

---

## Requirement Traceability Update

Not applied to `spec.md` (the Verifier writes only this report). Proposed statuses:

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| CAP-01 to CAP-12, CAP-14 to CAP-19, CAP-21, CAP-23 to CAP-34, CAP-36 to CAP-45 | Implementing | ✅ Verified |
| CAP-13, CAP-20, CAP-22, CAP-35 | Implementing | ❌ Needs a stronger test (behaviour correct) |
| CAP-46 | Implementing | ❌ Needs Fix |
| CAP-47 | Pending | Pending (closing step after a passing verdict) |

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 45/47 ACs have evidence matching the spec outcome; CAP-46 fails; CAP-47 pending by design; 1 spec-precision gap (CAP-17)
**Sensor**: 32/41 mutations killed; 4 blocking survivors (M07, M23, M25, M27), 3 non-blocking (M18, M19, M34), 2 by design (M40, M41)
**Gate**: 47 passed, 0 failed; pyright, ruff check, ruff format all exit 0

**What works**: tool list, annotations and schema; box and box model arithmetic; computed styles; sampled colours (order, limit, share, region); crop size, margin, clamping and downscale; default and explicit viewport width; shadow-root selectors; full-page pixels; context isolation; lazy launch; every error message; the timeout error and recovery; all gates.

**Issues found**: five fix tasks above, four of them test-only and one a one-line document change. No defect was found in the product code.

**Next steps**: apply Fix 1 to 5, re-verify, then mark slice 2 `concluída` in `docs/ROADMAP.md` (CAP-47).
