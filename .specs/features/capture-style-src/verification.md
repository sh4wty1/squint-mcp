# Measure a page whose policy refuses inline styles - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 962ebf2..5e28267
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Inputs: `plan.md`, `checks.md` (9 checks, `Profile: light`), issue #26 (`gh issue view 26 --repo sh4wty1/squint-mcp`, opened: body, no comments), and the diff `962ebf2..5e28267`, two commits: `b1576e0` (plan and checks) and `5e28267` (the build: `src/squint_mcp/js/stabilize.js`, `fill_text.js`, `covered_text.js`, `author_styles.js`; `tests/test_style_src.py`, `tests/fixtures/style-src.html`, `style-src.css`, `style-src-refused.html` new; `tests/fixtures/tokens-author.html` and `tests/test_extract_tokens.py` edited; `CHANGELOG.md`). The working tree is clean at `5e28267` before and after this run (`git status --porcelain` empty).

## Binding sources

Step 1 runs only under `ui`; not run. For the record: issue #26 names two routes (`bypass_csp=True`, or an error when the injected styles are refused) and asks for the maintainer's decision on the first. The plan's door 1 takes a third route, constructable sheets, and records both of the issue's routes as rejected with reasons; its "Expected" ("A Capture measures such a page as any other") is what AC 1-5 and C1-C6, C9 claim. The plan logs the route choice as an unconfirmed assumption (`Confirmed? n`) - a decision for the maintainer at review, not a contradiction a check carries.

## Checks

Verified at 5e28267. C1-C9 ran in one invocation:
`uv run pytest tests/test_style_src.py tests/test_extract_tokens.py -v -k "test_a_text_of_low_contrast_is_reported_under_the_policy or test_a_covered_text_is_reported_under_the_policy or test_a_text_in_an_open_shadow_root_is_reported_under_the_policy or test_the_policy_changes_no_finding or test_the_page_policy_still_refuses_its_own_inline_style or test_a_sheet_the_page_adopts_is_kept or test_a_page_with_no_style_says_its_values_are_the_defaults or test_a_shadow_root_with_no_style_is_no_author_style or test_a_transition_started_after_load_takes_no_time_under_the_policy"` - exit 0, **9 passed, 104 deselected in 18.89s** (`collected 113 items / 104 deselected / 9 selected`), each listed individually as PASSED. `rg -n "def test_"` finds the seven `test_style_src.py` tests at `:29`, `:35`, `:39`, `:45`, `:49`, `:55`, `:71` (file new in this diff) and the two `test_extract_tokens.py` tests at `:980` (C7, pre-existing, untouched by this diff) and `:991` (C8, added by this diff, hunk `@@ -988,6 +988,15 @@`). The fixture case `shadow` C8 names is added to `tests/fixtures/tokens-author.html` (`shadow: () => shadow(),`).

C1, C2, C3, C6 and C9 share one helper inside the test file, `one_finding` (`tests/test_style_src.py:23-26`): `(finding,) = await findings_on(...)` at `:25` fails unless exactly one Finding sits on the element's box (located through `inspect_element`, not the Finding's own selector), and `:26` asserts its check. That one-element unpack is what makes "exactly one" readable at the assertion.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | `style-src.html`, `low-contrast-real`: exactly one Finding on `#flat` | one invocation above, PASSED | `tests/test_style_src.py:32` - `await one_finding(client, "#flat", CONTRAST)`; `tests/test_style_src.py:25` - `(finding,) = await findings_on(client, PAGE, selector, findings)`; `:26` - `assert finding["check"] == checks[0]` | PASS |
| C2 | `style-src.html`, `overlap`: exactly one Finding on `#covered` (60% covered) | one invocation above, PASSED | `tests/test_style_src.py:36` - `await one_finding(client, "#covered", ["overlap"])`, settled by `:25`/`:26`; fixture geometry `tests/fixtures/style-src.css:18-19` (text 40-240px) and `:32-39` (cover 120-240px) = 120 of 200px | PASS |
| C3 | `style-src.html`, `low-contrast-real`: exactly one Finding on `#shadow-host span` in an open shadow root | one invocation above, PASSED | `tests/test_style_src.py:42` - `await one_finding(client, "#shadow-host span", CONTRAST)`, settled by `:25`/`:26` | PASS |
| C4 | same ordered `(selector, check)` list with and without the `<meta>` policy, and not empty | one invocation above, PASSED | `tests/test_style_src.py:67` - `assert under != []`; `:68` - `assert under == pairs((await detect(client, open_page))["findings"])` (list equality, so order and multiplicity); `:57` - `assert POLICY in source`, so the copy really lost the policy | PASS |
| C5 | `style-src-refused.html`, `inspect_element` on `#refused`: `computed.color` `rgb(0, 0, 0)`, not the inline `rgb(255, 0, 0)` | one invocation above, PASSED | `tests/test_style_src.py:78` - `assert result.structured_content["computed"]["color"] == "rgb(0, 0, 0)"` | PASS |
| C6 | page's own `document.adoptedStyleSheets` kept: exactly one Finding on `#adopted` | one invocation above, PASSED | `tests/test_style_src.py:46` - `await one_finding(client, "#adopted", CONTRAST)`, settled by `:25`/`:26`; the page sets the list at `tests/fixtures/style-src.html:24-26` | PASS |
| C7 | `tokens-author.html` with no style: `authorStyles: false` | one invocation above, PASSED | `tests/test_extract_tokens.py:986` - `assert result.structured_content["authorStyles"] is False` | PASS |
| C8 | `tokens-author.html?shadow`, open shadow root, no style: `authorStyles: false` | one invocation above, PASSED | `tests/test_extract_tokens.py:997` - `assert result.structured_content["authorStyles"] is False`; case `"shadow"` passed at `:994` | PASS |
| C9 | `#late`, 10s transition started 200ms after load: exactly one `low-contrast-real` Finding | one invocation above, PASSED | `tests/test_style_src.py:52` - `await one_finding(client, "#late", CONTRAST)`, settled by `:25`/`:26`; transition at `tests/fixtures/style-src.css:42-47`, class added at `tests/fixtures/style-src.html:27-29` | PASS |

## Coverage

Not recomputed: the `Coverage` join runs only under `standard` and `ui`. Read for the record: the three page scripts that add rules map to C9 (`stabilize.js`), C1 (`fill_text.js`) and C2 (`covered_text.js`); the two roots to C1/C3; the two kinds of the page's own style to C6/C5; the two roots `author_styles.js` skips in to C7/C8. `rg -n 'createElement\("style"\)' src/squint_mcp` returns nothing at HEAD, so no fourth page script still appends a `<style>`.

## Test policy rows

None: `checks.md` carries no `Test policy` section.

## Faults injected

Not owed under `light`. Because the brief asked whether any proof would pass under the old implementation, the Verifier ran these in a scratch copy outside the repo (`git archive HEAD` into the session scratchpad, real tree untouched, porcelain empty before and after):

| Mutation | Location | Killed |
| --- | --- | --- |
| all four page scripts reverted to `962ebf2` (`<style>` elements) | `src/squint_mcp/js/*.js` | yes - C1, C2, C3, C4, C6, C9 fail (6 failed, 3 passed); C5, C7, C8 pass, as guards should |
| stabilize rules appended as a `<style>` again, fills left as sheets | `src/squint_mcp/js/stabilize.js:28` | yes - C9 and C4 fail |
| `root.adoptedStyleSheets = [sheet]` (replace, not append) | `src/squint_mcp/js/stabilize.js:28` | yes - C6 fails |
| skip of `__squintSheets` removed | `src/squint_mcp/js/author_styles.js:16` | yes - C7 and C8 fail |

## Level and sampling

All nine proofs go through the MCP boundary against real Chromium: `detect_visual_bugs` via `tests/helpers.py` `detect`, `inspect_element` via `client.call_tool`, `extract_tokens` via `call`. That is the level the plan's AC name ("WHEN `detect_visual_bugs` is called ...").

- C4 reaches its claim: it compares the full ordered list of `(selector, check)` pairs, not a count, against a copy written to `tmp_path` that differs only by the removed `<meta>` line (with `style-src.css` and `Ahem.ttf` copied beside it), and guards against vacuity with `under != []`. Under the old scripts it fails at `:67` with `assert [] != []`.
- C5 and C8 pass under the old implementation too. That is expected: C5 is the guard against the rejected `bypass_csp` route (with `bypass_csp=True` the inline `rgb(255, 0, 0)` would apply), and C7/C8 guard that `author_styles.js` still leaves out Squint's own sheets; the last mutant above shows C7/C8 fail at HEAD when that skip goes.
- C7's test is pre-existing and untouched by the diff, but it runs the new `author_styles.js:16` path (the mutant kills it), so it does prove the new behaviour.

Implementation read against the checks:
- `stabilize.js:18` creates `globalThis.__squintSheets` (`WeakSet`); `stabilize.js:27-28`, `fill_text.js:22-23`, `covered_text.js:146-147` each add their sheet to it and append to `root.adoptedStyleSheets` with a spread, never replacing (door 1's literal shape). `fill_text.js` keeps one sheet per root in `globalThis.__squintFills` (a `WeakMap`) and `replaceSync`s it on each of the three fills.
- Order in `capture()`: `_STABILIZE` at `src/squint_mcp/capture.py:371` is the first page script after `goto` on the only Capture path, before `_AUTHOR_STYLES` (`:403`), the fills (`:409-411`) and covered text (`:419`), so the set exists before `fill_text.js`/`covered_text.js` call `.add` on it.

Observations (not gaps under `light`):
- `fill_text.js:22` and `covered_text.js:146` call `globalThis.__squintSheets.add(...)` without the `??=` that `stabilize.js:18` uses. If a page navigated itself between stabilize and the fills, the new document's globals would lack the set and the fill would throw a `TypeError` where the old code appended a `<style>`. The old code would already have lost its stabilize styles there, and no check claims that case; a robustness note only.
- The C1/C3/C6/C9 claims name the fixture's colour (`rgb(119, 119, 119)`, 4.47:1); that value lives in the fixture (`style-src.css:22-25`, `style-src.html:25`), not in the assertion. It is a precondition, not the asserted value, so not a precision gap.

## Swept existing

`checks.md` `## Swept` has no `existing` rows; every row is `n/a` or cites C1, C2, C5, C9, all proven above. Re-read against the diff: "no new input" holds (no tool argument changes in the diff); "a Capture opens a fresh context on every call" holds (`src/squint_mcp/capture.py:351` `context = await browser.new_context(` inside each `capture()` call); "no new dependency" holds (`CSSStyleSheet`/`adoptedStyleSheets` are browser built-ins, no `pyproject.toml` change in the diff).

## Gate

All run by the Verifier at HEAD `5e28267`, working tree clean.

- `uv run pyright` - exit 0, `0 errors, 0 warnings, 0 informations`
- `uv run ruff check` - exit 0, `All checks passed!`
- `uv run ruff format --check` - exit 0, `144 files already formatted`
- `uv run pytest -q -p no:cacheprovider` - exit 0, `564 passed in 1794.09s (0:29:54)`. A first background run of the suite was cut off without a summary line (no python process left, 43 progress dots in its log); this second run is the one counted.
