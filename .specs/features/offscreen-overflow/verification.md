# `offscreen-overflow` verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 9923762..d84cce9
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

All 21 checks are proven at `d84cce9bd5c336f241216f656435ca17f87c8644` with a located assertion each, and the gate is green. Three precision gaps are recorded after the checks table; none of them fails a check as written.

## Profile scope

`checks.md` was approved under `light`, so these steps ran: every proof at `HEAD`, each named test shown to exist and to have run, one located assertion per check, the level and sampling judgment, and the re-read of the `Swept` rows that resolve to existing code. These did not run, by profile: step 1 (binding sources, `ui`), the recompute of the `Coverage` join and the `Test policy` verdicts (`standard`, `ui`; `checks.md` carries no `Test policy` section either), and fault injection (`standard`, `ui`). Step 5 does not apply: no flow here is decided by human judgment.

## Checks

The 21 pytest node ids of C1 to C18 ran in one invocation, `uv run pytest -v <21 node ids>`: 25 lines, each `PASSED`, `25 passed in 18.02s`, exit 0. Each named test was shown individually; the parametrized ones showed 2 lines (C6) and 4 lines (C11). `T` is `tests/test_offscreen_overflow.py`, `D` is `tests/test_detect_visual_bugs.py`.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | `bug` at 1440x900 yields exactly one Finding, on `#wide`, with the four fixed values | `T::test_a_page_wider_than_its_viewport_yields_one_finding` PASSED | `tests/test_offscreen_overflow.py:32` - `(finding,) = (await detect(client, BUG, checks=ONLY))["findings"]`; `:33` - `assert finding["selector"] == "#wide"`; `:34` - `assert finding["check"] == "offscreen-overflow"`; `:35` - `assert finding["category"] == "responsive"`; `:36` - `assert finding["severity"] == "major"`; `:37` - `assert finding["source"] == "Squint heuristic"` | PASS |
| C2 | that Finding carries the three widths, the four styles and the message | `T::test_the_finding_carries_the_widths_and_the_styles_that_explain_it` PASSED | `tests/test_offscreen_overflow.py:44` - `assert finding["message"] == ("Extends 200px past the 1440px viewport, so the page scrolls horizontally")`; `:47` - `assert finding["evidence"]["measured"] == {"overflowPx": 200, "pageWidth": 1640, "viewportWidth": 1440}`; `:52` - `assert finding["evidence"]["computed"] == {"display": "block", "position": "static", "width": "1640px", "white-space": "normal"}` | PASS |
| C3 | on `nested` the one Finding is on `#outer`, not on its child at the same edge | `T::test_an_element_at_the_edge_is_named_instead_of_its_child_at_the_same_edge` PASSED | `tests/test_offscreen_overflow.py:64` - `assert [finding["selector"] for finding in findings] == ["#outer"]` | PASS |
| C4 | on `child` the one Finding is on `#child`, its parent fitting | `T::test_a_child_at_the_edge_is_named_instead_of_its_parent_that_fits` PASSED | `tests/test_offscreen_overflow.py:71` - `assert [finding["selector"] for finding in findings] == ["#child"]` | PASS |
| C5 | on `near` the one Finding is on `#edge`, not on `#near` 1px short | `T::test_an_element_one_pixel_short_of_the_edge_is_not_the_one_named` PASSED | `tests/test_offscreen_overflow.py:78` - `assert [finding["selector"] for finding in findings] == ["#edge"]` | PASS |
| C6 | an element under 1px from the edge is named on either side: `overflowPx` 201 on a page of 601, 200 on a page of 600 | `T::test_an_element_under_a_pixel_from_the_edge_is_named` PASSED for `[fraction-short-601]` and `[fraction-past-600]`, 2 of 2 cases | `tests/test_offscreen_overflow.py:82` - `[("fraction-short", 601), ("fraction-past", 600)]`; `:87` - `(finding,) = await small(client, name)`; `:88` - `assert finding["selector"] == "#fraction"`; `:89` - `assert finding["evidence"]["measured"] == {"overflowPx": page_width - 400, "pageWidth": page_width, "viewportWidth": 400}` | PASS |
| C7 | on `word` the one Finding is on `#word`, `box` 200px wide, `overflowPx == 200` | `T::test_a_word_that_cannot_break_names_the_element_whose_text_it_is` PASSED | `tests/test_offscreen_overflow.py:99` - `(finding,) = await small(client, "word")`; `:100` - `assert finding["selector"] == "#word"`; `:102` - `assert finding["box"]["w"] == 200`; `:103` - `assert finding["evidence"]["measured"]["overflowPx"] == 200` | PASS |
| C8 | on `moved` the one Finding has the painted `box` and `overflowPx == 150` | `T::test_an_element_moved_by_a_transform_is_reported_where_it_is_painted` PASSED | `tests/test_offscreen_overflow.py:109` - `(finding,) = await small(client, "moved")`; `:110` - `assert finding["box"] == {"x": 450, "y": 0, "w": 100, "h": 20}`; `:111` - `assert finding["evidence"]["measured"]["overflowPx"] == 150` | PASS |
| C9 | one call on `one` at 399 and at 400 yields exactly one Finding, at 399, with the three widths | `T::test_one_pixel_past_the_viewport_is_reported_and_none_is_not` PASSED | `tests/test_offscreen_overflow.py:121` - `(finding,) = content["findings"]` over `viewports=[narrower, SMALL]` (`:119`); `:122` - `assert finding["viewport"] == narrower`; `:123` - `assert finding["evidence"]["measured"] == {"overflowPx": 1, "pageWidth": 400, "viewportWidth": 399}` | PASS |
| C10 | `clean` at 1440x900 yields no Finding, with seven near misses on the page | `T::test_a_page_as_wide_as_its_viewport_yields_no_finding` PASSED | `tests/test_offscreen_overflow.py:131` - `assert (await detect(client, page("clean")))["findings"] == []`. The seven members sit in `tests/fixtures/offscreen-overflow-clean.html:17` (`#left`), `:22` (`#fixed`), `:29` (`#clipper`), `:36` (`#scroller`), `:43` (`#shadow`), `:47` (`#margin`), `:52` (`#tall`). See precision gap 1 | PASS |
| C11 | no Finding when `overflow-x` is `hidden` or `clip` on `html`, or on `body` under a `visible` `html` | `T::test_a_page_that_hides_its_horizontal_overflow_yields_no_finding` PASSED for `[hidden-html]`, `[clip-html]`, `[hidden-body]`, `[clip-body]`, 4 of 4 cases | `tests/test_offscreen_overflow.py:135` - `"name", ["hidden-html", "clip-html", "hidden-body", "clip-body"]`; `:140` - `assert await small(client, name) == []`. See precision gap 1 | PASS |
| C12 | on `rtl` there is no Finding | `T::test_a_right_to_left_page_yields_no_finding` PASSED | `tests/test_offscreen_overflow.py:152` - `assert await small(client, "rtl") == []`. See precision gap 1 | PASS |
| C13 | on `pseudo` there is no Finding | `T::test_a_page_widened_by_a_pseudo_element_yields_no_finding` PASSED | `tests/test_offscreen_overflow.py:158` - `assert await small(client, "pseudo") == []`. See precision gap 1 | PASS |
| C14 | naming the Check on `bug` returns its Finding alone | `T::test_naming_the_check_returns_its_finding_alone` PASSED | `tests/test_offscreen_overflow.py:163` - `assert [(finding["selector"], finding["check"]) for finding in findings] == [("#wide", "offscreen-overflow")]` | PASS |
| C15 | no `checks` on `bug` returns both Findings, both `major`, in that order | `T::test_omitting_checks_returns_the_findings_of_every_check` PASSED | `tests/test_offscreen_overflow.py:172` - `assert [(finding["selector"], finding["check"]) for finding in findings] == [("#wide", "offscreen-overflow"), ("#clipped", "text-clipped")]`; `:176` - `assert {finding["severity"] for finding in findings} == {"major"}` | PASS |
| C16 | the error for an unknown name holds the list of three in each of the four tests that quote it | `D::test_unknown_check_is_an_error_listing_the_valid_ones`, `D::test_unknown_check_after_a_valid_one_is_still_an_error`, `D::test_the_first_unknown_check_in_the_order_given_is_the_one_named`, `D::test_unknown_check_is_reported_before_any_browser_work` each PASSED; the `grep -c` proof printed `4` | `tests/test_detect_visual_bugs.py:341` - `'Unknown check "nope". ' "Valid checks: low-contrast-real, offscreen-overflow, text-clipped." in text`; the same expression at `:351`; `:361` with `"zzz"`; `:372`. See precision gap 2 | PASS |
| C17 | the description of `detect_visual_bugs` names `offscreen-overflow` and what it reports | `T::test_the_tool_description_says_what_offscreen_overflow_reports` PASSED | `tests/test_offscreen_overflow.py:185` - ``assert ("`offscreen-overflow` (the element that sets the width of a page that " "scrolls horizontally") in " ".join(tool.description.split())`` | PASS |
| C18 | the test files of `9923762` lose exactly four lines, and `inspect_element` keeps its six keys with `Element` carrying `tag` | the `git diff ... grep -c "^-[^-]"` proof printed `4`, over all nine test files that exist at `9923762`; `tests/test_inspect_element.py::test_structured_content_has_exactly_the_documented_keys` PASSED | the four removed lines are the old assertions now at `tests/test_detect_visual_bugs.py:341`, `:351`, `:361`, `:372`; `tests/test_inspect_element.py:285` - `assert set(content) == {"viewport", "stabilized", "box", "boxModel", "computed", "sampledColors"}`; `src/squint_mcp/models.py:49` - `tag: str`, a required field of `Element` | PASS |
| C19 | `CHANGELOG.md` has the entry under `[Unreleased]`, `### Added`, with the three phrases | the three `sed ... grep -c` proofs printed `1`, `1`, `1` | `CHANGELOG.md:11` - ``- `offscreen-overflow` Check: ... one per viewport ... Its severity is always `major`. It reports nothing while the page hides its horizontal overflow ...``, under `### Added` at `CHANGELOG.md:9` and `## [Unreleased]` at `CHANGELOG.md:7`, above `## [0.1.0]` at `CHANGELOG.md:18` | PASS |
| C20 | the sentence of `README.md` reads `runs three Checks` and names `offscreen-overflow` | the first `grep` proof printed `1`, the second printed `0` | `README.md:45` - ``` `detect_visual_bugs` runs three Checks: `text-clipped` (...), `low-contrast-real` (...) and `offscreen-overflow` (the element that makes the page scroll horizontally) ``` | PASS |
| C21 | type check, lint, format and the whole suite are green | `uv run pyright` exit 0; `uv run ruff check` exit 0; `uv run ruff format --check` exit 0; `uv run pytest` exit 0 | the commands of `.github/workflows/ci.yml:18`, `:20`, `:22`, `:24`: `0 errors, 0 warnings, 0 informations`; `All checks passed!`; `92 files already formatted`; `233 passed in 366.66s` | PASS |

## Level and sampling

- **Level.** C1, C2, C14, C15 and C16 name a response shape or an error text. Every one of their proofs reaches the tool through the MCP client: `tests/helpers.py:28` - `return await client.call_tool("detect_visual_bugs", {"url": url, **extra})`, on the client of `tests/conftest.py:26` - `async with Client(server) as connected`. C17 reads the description through `client.list_tools()` at `tests/test_offscreen_overflow.py:182`. No proof sits below the boundary its claim names: no level gap.
- **Sampling.** C6 claims 2 cases and ran 2; C11 claims 4 and ran 4; C16 claims four tests and ran four. C10 carries seven members on one assertion: all seven are in the fixture (lines cited in its row). No check claims more cases than its proof exercises: no sampling gap.
- **Touched by the feature.** `tests/test_offscreen_overflow.py` is new in the range and the four assertions of C16 are edited in it. The second proof of C18 resolves to `tests/test_inspect_element.py`, which the range does not touch; that is what the claim is about (an output that must not change while `Element` gains a field), so the untouched test is the right proof and not an empty one.
- **A test no check names.** `tests/test_offscreen_overflow.py:143` `test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named` asserts `[finding["selector"] for finding in findings] == ["body"]` at `:148`. It pins the other side of AC 11 (a `body` that hides its overflow under an `html` that is not `visible` is still reported). It ran green inside C21 (21 of the 233 are this file: 17 functions, 4 extra parametrized cases), but no check owns it, so nothing in `checks.md` would notice if it were deleted.

## Swept rows that resolve to existing code

- validation (C16): `src/squint_mcp/tools/detect_visual_bugs.py:80` - `raise ToolError(f'Unknown check "{name}". Valid checks: {valid}.')`, with `valid = ", ".join(sorted(CHECKS))` at `:79` and the new name registered at `src/squint_mcp/checks/__init__.py:17`. There.
- failure modes (C13): `src/squint_mcp/checks/offscreen_overflow.py:86` - `return []` after the loop finds no element at the edge. The reach of an element with no box is `element.box.x + element.box.w` at `:37`, which is 0, and the loop is only reached when `page_width > capture.viewport.width` (`:75`), so its distance to the edge is never under 1. There.
- idempotency (`n/a`, cites a test): `tests/test_detect_visual_bugs.py:126` `test_the_same_call_returns_the_same_structured_content` exists and ran green inside C21.
- dependency failure (`n/a`, cites ADR-0002): `docs/adr/0002-checks-consume-captures-only.md` exists, and `src/squint_mcp/checks/offscreen_overflow.py:3` and `:4` import only `config` and `models`.
- the other rows say `n/a`: approved policy, nothing in the code for them to be wrong about.

## Precision gaps

None of these fails a check. Each is a finding about the checks or about a test.

| Gap | Where | What the proof leaves open | Weight |
| --- | --- | --- | --- |
| 1. A no-Finding proof does not assert the precondition its claim names | C10, C11, C12, C13 - `tests/test_offscreen_overflow.py:131`, `:140`, `:152`, `:158` | Each claim names what makes the page a real case (C11: "a page of 600px in `pixels` whose `#wide` ends at its right edge"; C12 and C13 likewise; C10: "the page is 1440px wide"), and each proof asserts only `== []`. That expression is also true on a page that is not wider than its viewport, where the Check returns at `src/squint_mcp/checks/offscreen_overflow.py:75` before reading `overflow-x`, `direction` or any element. The only backing for the widths is the author's measurement quoted in the header of `checks.md`. A fixture edit, or a Chromium whose full-page screenshot stops covering hidden overflow, turns C11, C12 and C13 into green proofs of nothing, and no assertion moves | medium |
| 2. C16 says "holds" where AC 16 says "SHALL end with" | C16 - `tests/test_detect_visual_bugs.py:341`, `:351`, `:361`, `:372` | The four assertions are substring membership (`... in text`). Text appended after `text-clipped.` would pass all four and the `grep -c` proof. The code does end the message there (`src/squint_mcp/tools/detect_visual_bugs.py:80`); no proof says so | low |
| 3. C6 states the declared widths, and its two cases sit about 0.4px from the edge | C6 - `tests/test_offscreen_overflow.py:82` | The claim reads "600.6px" and "600.4px"; Chromium paints them at 600.594 and 600.391 (measured below), 0.406px short of a page of 601 and 0.391px past one of 600. With C5 at exactly 1px, the proofs hold `OFFSCREEN_OVERFLOW_EDGE_TOLERANCE_PX` (`src/squint_mcp/config.py:89`) between about 0.41 and 1: a tolerance of 0.5 passes every proof. Likely immaterial, since the page width is a whole number of pixels and an element setting it cannot be far past half a pixel from it, but "under 1px" is not what is pinned | low |

### Measurement behind gap 1

Not a step of another profile and no mutation: a throwaway script in the scratch directory called `capture()` and the Check's own `_reach` and `_scrolls_right` on the fixtures at `d84cce9`, reading the tree only. It answers whether the four no-Finding proofs are empty today. They are not: every precondition the claims name holds, and in C11 and C12 an element sits on the edge that would be named if the suppression were gone.

| Fixture | Viewport width | `pixels.width` | Elements within 1px of the page's right edge | `_scrolls_right` | Named |
| --- | --- | --- | --- | --- | --- |
| `clean` (C10) | 1440 | 1440 | not reached: page not wider (`#fixed`, `#cut`, `#scrolled` reach 1640; `#left` reaches 200) | True | none |
| `hidden-html` (C11) | 400 | 600 | `#wide` at 600 | False | none |
| `clip-html` (C11) | 400 | 600 | `#wide` at 600 | False | none |
| `hidden-body` (C11) | 400 | 600 | `#wide` at 600 | False | none |
| `clip-body` (C11) | 400 | 600 | `#wide` at 600 | False | none |
| `rtl` (C12) | 400 | 600 | `#pinned` at 600 | False | none |
| `pseudo` (C13) | 400 | 600 | none (`html`, `body`, `#host` reach 400) | True | none |
| `fraction-short` (C6) | 400 | 601 | `#fraction` at 600.594 | True | `#fraction` |
| `fraction-past` (C6) | 400 | 600 | `#fraction` at 600.391 | True | `#fraction` |

## Gate

`uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
`uv run ruff check` - All checks passed!, exit 0
`uv run ruff format --check` - 92 files already formatted, exit 0
`uv run pytest` - 233 passed, 0 failed, in 366.66s, exit 0

The real tree's `git status --porcelain` was empty before the run and after it, this report aside.
