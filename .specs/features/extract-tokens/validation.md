# extract-tokens Validation

**Date**: 2026-10-14
**Spec**: `.specs/features/extract-tokens/spec.md` (TOK-01 to TOK-79)
**Diff range**: `f2c6213..e3fcf12` as given (branch `feat/extract-tokens`). That range also holds slices 6 to 9; the surface of this feature is `ee2c88e..e3fcf12` (from `6e85ca4`, the first commit of its spec): 21 files under `src/` and `tests/`, among them `src/squint_mcp/tokens.py`, `color.py`, `tools/extract_tokens.py`, `capture.py`, `js/collect_elements.js`, `js/srgb_colors.js`, `config.py`, `models.py`, `server.py`, `tests/test_extract_tokens.py`, `tests/test_color.py` and seven fixtures.
**Verifier**: independent sub-agent (author ≠ verifier), first pass

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

All 79 criteria have an assertion at `file:line` that targets the outcome the spec gives, and the Full gate is green (75 passed). The discrimination sensor injected 22 behaviour-level mutants: 18 were killed and 4 survived. The 4 survivors are 3 gaps. In each one the code does what the Terms say, but no fixture gives a different result when the rule is dropped:

1. A `scope` is not held for `typography`, `radii` and `shadows` (mutant S2). This is the maintainer's point (1).
2. The order of the `colors` Tokens by the summed Uses of their Group is not held (mutants C1 and C2). This is the maintainer's point (2).
3. The clause of Painted text that says "when at least one of them paints a box" is not held (mutant P1).

Two spec-precision gaps are flagged. One is the fixture of TOK-56, which is the same as gap 1 seen from the spec. The other is what "the message" of a failure is, which is the maintainer's point (3) and does not block.

Abbreviations: `T` = `tests/test_extract_tokens.py`, `K` = `src/squint_mcp/tokens.py`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T29 | ✅ Done | Every box is ticked in `tasks.md`. Checked against the files, not against the notes. |
| T30 | ⏳ Pending | Waits for a PASS, by design (`tasks.md:1214-1231`). Not counted as a gap. |

---

## Spec-Anchored Acceptance Criteria

The `extract` helper (`T:39-48`) runs on every successful call. It asserts `is_error is False`, then `assert_sums_hold` (`T:64-81`, which covers TOK-13 and TOK-14), then at most 20 Tokens per Family (`T:46-47`, which covers TOK-66). The `fail` helper (`T:51-61`) asserts `is_error is True`, `structured_content is None` and one text block (which covers TOK-72). It then strips the SDK prefix and returns the rest.

### P1: Read the tokens of a page

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-01 | 5 colour tuples, whole and in order | `T:187` `rows(colors, *fields) == [("#333333",3,3,0,0), …]`; `T:195` single variants | ✅ PASS (see gap 2: the order is not told apart from build order) |
| TOK-02 | `(Arial, sans-serif, 5)` alone | `T:207` `== [("Arial, sans-serif", 5)]` | ✅ PASS |
| TOK-03 | `(14,3),(16,1),(32,1)` | `T:212` | ✅ PASS |
| TOK-04 | `(400,2),(700,3)` | `T:217` | ✅ PASS |
| TOK-05 | `(20,3),(24,1),(40,1)` | `T:223` | ✅ PASS |
| TOK-06 | 3 spacing tuples with roles | `T:231` | ✅ PASS |
| TOK-07 | `(4px,1),(8px,1)` | `T:241` | ✅ PASS |
| TOK-08 | `(box, rgba(0, 0, 0, 0.2) 0px 1px 3px 0px, 1)` alone | `T:247` | ✅ PASS |
| TOK-09 | viewport 1440x900, stabilized true, scope null, elements 8, total = len | `T:165-171` | ✅ PASS |
| TOK-10 | exact summary text | `T:257` `block.text == "Tokens: colors 5, …; stabilized."` | ✅ PASS |
| TOK-11 | one block, no image | `T:177-178` `(block,) = result.content`; `isinstance(block, TextContent)` | ✅ PASS |
| TOK-12 | equal structured content | `T:268` `first == second` | ✅ PASS |
| TOK-13 | uses = sum of variants; value = first variant | `T:77-78`, on every `extract` call (`T:45`) | ✅ PASS |
| TOK-14 | uses = sum of roles (colors, spacing) | `T:81` | ✅ PASS |

### P1: Count a value only where it paints

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-15 | `#aa0000` uses 1, text 1 | `T:277` | ✅ PASS |
| TOK-16 | `#222222` text 1; no `#111111` | `T:282-283` | ✅ PASS |
| TOK-17 | no value starting `#008080` | `T:288` (over Tokens and variants) | ✅ PASS |
| TOK-18 | no `#445566…`, no 8-digit `…00` | `T:293-294` | ✅ PASS |
| TOK-19 | `#00000080`, background 1 | `T:302` | ✅ PASS |
| TOK-20 | `#0000aa` uses 1, border 1; no `#00aa00` | `T:310`, `T:312` | ✅ PASS |
| TOK-21 | four border Tokens, border 1 each | `T:317-318` | ✅ PASS |
| TOK-22 | no `#aa00aa` | `T:451` | ✅ PASS |
| TOK-23 | no `#00aaaa` | `T:457` | ✅ PASS |
| TOK-24 | none of the 3 colours; none of the 3 elements counted | `T:464-468` (`elements == 31`); `T:783-784` (each alone gives 0) | ✅ PASS |
| TOK-25 | no 40/900/50/Georgia in any typography list; sizes holds 12 | `T:339-342` | ✅ PASS |
| TOK-26 | sizes holds 13; line-height uses = size uses − 1 | `T:348-352` | ✅ PASS |
| TOK-27 | lineHeights holds 30 | `T:360` | ✅ PASS |
| TOK-28 | 51/53/55/57, uses 1, margin 1 | `T:365-367` | ✅ PASS |
| TOK-29 | 61/63/65/67, uses 1, padding 1 | `T:372-374` | ✅ PASS |
| TOK-30 | no 620 | `T:381` | ✅ PASS |
| TOK-31 | nothing ≤ 0; no 71 | `T:386-387` | ✅ PASS |
| TOK-32 | 81, 83 with gap 1 | `T:392-393` | ✅ PASS |
| TOK-33 | 85/87/89, uses 1, gap 1 | `T:401-403` | ✅ PASS |
| TOK-34 | no 91 | `T:408` | ✅ PASS |
| TOK-35 | 41/43/45/47px, uses 1; no `0px` | `T:415-418` | ✅ PASS |
| TOK-36 | `50%`, `10px 20px` uses 1, after every px Length | `T:427` (last two rows); `T:530-537` (whole list) | ✅ PASS |
| TOK-37 | `(text, rgb(0, 0, 0) 1px 1px 2px)` uses 1 | `T:436` | ✅ PASS |
| TOK-38 | one box Token of the two-layer text, uses 1 | `T:444` | ✅ PASS |
| TOK-39 | holds `#336699` | `T:324` (a Token `value`) | ✅ PASS |
| TOK-40 | holds `#ff0000` | `T:331` | ✅ PASS |

### P1: Fold values that are nearly equal

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-41 | `#1a73e8` uses 7, roles {1,6,0}, variants `(#1a73e8,4),(#1a78e8,3)` | `T:550-556` | ✅ PASS |
| TOK-42 | `#1a79e8` uses 1, single variant | `T:565-567` | ✅ PASS |
| TOK-43 | `#1a73e880` uses 1, apart from `#1a73e8` | `T:573-575` | ✅ PASS |
| TOK-44 | `#808080` uses 4, variants `(#808080,2),(#858585,2)` | `T:584-589` | ✅ PASS |
| TOK-45 | `(15,1),(16,4),(17,4)` | `T:595` | ✅ PASS |
| TOK-46 | variants of 17: `(17,2),(16.75,1),(17.75,1)` | `T:603` | ✅ PASS |
| TOK-47 | variants of 16: `(16,3),(16.5,1)` | `T:616` | ✅ PASS |
| TOK-48 | `8` uses 3, padding 3, variants `(8,2),(8.5,1)` | `T:634-636` | ✅ PASS |
| TOK-49 | `4px` uses 3, variants `(4px,2),(4.5px,1)` | `T:641-645` | ✅ PASS |
| TOK-50 | one Token `20`, variants end `(20.5,1)` | `T:652-654` | ✅ PASS |
| TOK-51 | four Tokens of uses 1 | `T:626-629` | ✅ PASS |

### P1: Narrow the reading to a part of the page

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-52 | 4 colour rows in order; scope `.card` | `T:712-718` | ✅ PASS |
| TOK-53 | elements 6 | `T:724` | ✅ PASS |
| TOK-54 | holds `#ff0000`; elements 9 | `T:730-732` | ✅ PASS (note: `values()` also accepts a variant; this is equivalent here, since no two colours of the page are Near) |
| TOK-55 | `(#00ffff,1)` alone; elements 1 | `T:737-738` | ✅ PASS |
| TOK-56 | every Family but `colors` `{total: 0, tokens: []}` | `T:743-744` | ⚠️ Spec-precision gap: the outcome is the same with no scope (see point 1) |
| TOK-57 | message `Scope ".missing" matched no elements.` | `T:749` `message == …` (after the SDK prefix) | ✅ PASS (see point 3) |
| TOK-58 | message `Invalid selector "div[".` | `T:753` | ✅ PASS (see point 3) |
| TOK-59 | elements 0; every Family empty | `T:761-763` | ✅ PASS |
| TOK-60 | exact zero summary | `T:769` | ✅ PASS |
| TOK-61 | fails; not a whole-page reading | `T:776-777` (fails, and the message is not a summary) | ✅ PASS (the spec gives no message, and none is asserted) |

### P2: Bound the response

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-62 | total 21; 10…190, then 210 | `T:793-794` | ✅ PASS |
| TOK-63 | total 20; 10…200 | `T:799-800` | ✅ PASS |
| TOK-64 | total 21; first 20 by text, in order | `T:808-830` (exact list; the fixture has 21 backgrounds, `#ffffff` the last) | ✅ PASS |
| TOK-65 | the text says `colors 21` and `spacing 21` | `T:837-838` | ✅ PASS |
| TOK-66 | ≤ 20 per Family | `T:46-47`, on every `extract` call | ✅ PASS |

### P2: Tool contract, config and documents

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-67 | hints, output schema, `url` required, `scope` optional string, viewport min 1 | `T:131-158` | ✅ PASS |
| TOK-68 | holds `#111111`, not `#999999`; viewport 375x812 | `T:847-849` | ✅ PASS (same `values()` note as TOK-54) |
| TOK-69 | exact scheme message | `T:853` | ✅ PASS (see point 3) |
| TOK-70 | starts with `Could not load ` + url | `T:860` | ✅ PASS (see point 3) |
| TOK-71 | `Timed out after 30s.` | `T:872` `== "Timed out after 1s."` with the config set to 1.0. The 30 is `config.py:8` (`TOTAL_TIMEOUT_S = 30.0`), formatted by `tools/extract_tokens.py:68` (`{:g}s`) | ✅ PASS |
| TOK-72 | error, no structured content | `T:55-56`, in every `fail` call | ✅ PASS |
| TOK-73 | stabilized false; the text ends `; not stabilized.` | `T:883-885` | ✅ PASS |
| TOK-74 | 34 published pairs to four places | `tests/test_color.py:18` (34 rows), `tests/test_color.py:21-22` (both orders) | ✅ PASS |
| TOK-75 | three named constants, each with its source | `src/squint_mcp/config.py:191-205` (read) | ✅ PASS |
| TOK-76 | README describes the tool; CHANGELOG under Unreleased | `README.md:44`, `README.md:48-53`; `CHANGELOG.md:7`, `CHANGELOG.md:11` (read) | ✅ PASS |
| TOK-77 | earlier tests pass, with only the two tool lists changed | `git diff ee2c88e..e3fcf12` on earlier tests: only `tests/test_ping.py:38` and `tests/test_inspect_element.py:466` gain `extract_tokens` (and the ping test's name). The Build was not re-run here, by the orchestrator's instruction: 496 passed at `1c1b55f`, as recorded under T29 | ✅ PASS |

### Edge Cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-78 | `40` uses 2, variants `(40,1),(40.5,1)` | `T:694-696` | ✅ PASS |
| TOK-79 | `8` uses 1, margin 1 | `T:702-703` | ✅ PASS |

**Status**: All 79 criteria are covered, with the assertion on the spec's outcome. ⚠️ 2 spec-precision gaps are flagged (TOK-56; the meaning of "message" in TOK-57, 58, 69, 70 and 71). Two rules of the Terms have no criterion whose fixture tells them apart: the Family order of `colors`, and the box clause of Painted text. The sensor found both.

---

## Discrimination Sensor

**Depth**: expanded (22 mutants), because the tool changes what every Capture reads.

**Isolation**: a detached worktree at `C:\Users\Dev\AppData\Local\Temp\tok-verify` (`e3fcf12`). Each mutant was applied by exact string replacement, checked to occur once. The tests ran with the repo's `.venv` and `PYTHONPATH` set to the worktree's `src`; `squint_mcp.tokens.__file__` was checked to resolve there. After each run `git checkout -- src` reset the worktree. At the end the worktree was removed with `git worktree remove --force` and `git worktree prune`. `git status --porcelain` of the real tree was empty before and empty after (byte-identical), and HEAD stayed at `e3fcf12`. Each mutant ran the whole Quick gate: `pytest tests/test_color.py tests/test_extract_tokens.py`.

| # | File:line | Description | Killed? | Killed by |
| - | --------- | ----------- | ------- | --------- |
| S1 | `tools/extract_tokens.py:71-72` | With a scope, the seven non-colour Families read from a second Capture of `*` (the whole page) | ✅ Killed | only `T:797` (TOK-63, spacing) |
| S2 | `tools/extract_tokens.py:71-72` | As S1, but `spacing` stays scoped: typography, radii and shadows read from the whole page | ❌ **Survived** | - |
| C1 | `K:233` | `colors` Tokens kept in build order (the order their Groups were opened), then cut at the Limit | ❌ **Survived** | - |
| C2 | `K:233` | `colors` Tokens ranked by the Uses of their Representative, not of their Group | ❌ **Survived** | - |
| G1 | `K:147` | A Value joins the first Near Group, not the nearest | ✅ Killed | `T:592`, `T:598`, `T:610`, `T:657` |
| G2 | `K:147` | A tie goes to the Group opened last (`<` → `<=`) | ✅ Killed | `T:592`, `T:598`, `T:610`, `T:657` |
| G3 | `K:287` | Lengths exactly 1px apart are Near | ✅ Killed | `T:345`, `T:471`, `T:592`, `T:598`, `T:610`, `T:657` |
| G4 | `K:146` | A Value is compared with every member of a Group, not only its Representative | ✅ Killed | `T:544`, `T:559`, `T:592`, `T:598`, `T:610`, `T:657` |
| G5 | `K:244` | Colours of different alphas can be Near | ✅ Killed | `T:544`, `T:570`, `T:657` |
| G6 | `K:249` | Colour threshold loosened to ΔE 2.3 | ✅ Killed | `T:544`, `T:559`, `T:657` |
| R1 | `K:131` | Rank order ties broken by Value descending | ✅ Killed | `T:578`, `T:598`, `T:657`, `T:691` |
| U1 | `K:125` | One Use per side/corner/axis instead of one per Value per element | ✅ Killed | 12 tests (e.g. `T:181`, `T:226`, `T:238`) |
| P1 | `K:265` | Painted text = Own text, whether or not it paints a box | ❌ **Survived** | - |
| P2 | `K:209` | Text colour read from `color`, not `-webkit-text-fill-color` | ✅ Killed | `T:280`, `T:291`, `T:471` |
| P3 | `K:259` | The opacity of ancestors ignored | ✅ Killed | `T:454`, `T:460`, `T:471` |
| P4 | `K:345` | `auto` margins counted | ✅ Killed | `T:377`, `T:471` |
| P5 | `K:433` | `elements` counts every element of the Capture, not the Read ones | ✅ Killed | 9 tests (e.g. `T:161`, `T:721`, `T:756`) |
| L1 | `K:176` | The Limit cut after Family order, not in Rank order | ✅ Killed | `T:787` |
| E1 | `tools/extract_tokens.py:64-65` | An empty scope read as no scope | ✅ Killed | `T:775` |
| E2 | `tools/extract_tokens.py:70` | The no-match failure raised as a `ValueError` (a crash), not a `ToolError` | ✅ Killed | `T:747` (the prefix assertion in `fail`) |
| D1 | `src/squint_mcp/js/collect_elements.js:204` | The descendants of a match do not enter open shadow trees | ✅ Killed | `T:706`, `T:721` |
| X1 | `src/squint_mcp/color.py:136` | ΔE2000 without the rotation term `R_T` | ✅ Killed | `tests/test_color.py:12`, `T:544`, `T:559`, `T:657` |

**Result**: 18 of 22 killed, 4 survived (3 gaps). ❌ FAIL

None of the four survivors is equivalent. Each one changes what a call returns on a page the spec's Terms describe:

- S2: a scoped call on a page whose text, radii or shadows lie outside the scope.
- C1 and C2: a page where a later-opened Group's summed Uses pass those of an earlier Representative.
- P1: an element whose Own text paints no box, in a box that does.

---

## The three points the maintainer asked about

### Point 1: does TOK-56's test tell a scope from the whole page? Verdict: **gap**

No. `tokens-scope.html` gives no element text of its own, and no margin, padding, radius or shadow (its own comment and the spec's TOK-52 preamble). Only `background-color` is set. So the whole page leaves the seven non-colour Families empty too. `T:741-744` holds for `#one-child`, and it would hold just the same for no scope at all. TOK-59 (`T:756-763`, `#gone`) has the same blind spot: an empty Family is empty either way on this page.

The literal mutant, "ignore scope for the non-colour Families" (S1), is killed, but only by TOK-63 (`T:797-800`, `scope="#twenty"` on `tokens-limit.html`), because `spacing` differs there. The narrower mutant S2 leaves `spacing` scoped and reads typography, radii and shadows from the whole page. It passes all 75 tests: no scoped call anywhere in the module reads those Families on a page where the whole page differs.

The code itself is sound: every Family is computed from the same `read` list (`K:431-438`), and the Capture alone narrows it. But a per-Family scope bug is not held. This is a spec-precision gap, because the fixture the spec fixes for TOK-56 cannot fail the rule.

**Fix**: give `tokens-scope.html` one element outside every card, for instance `#outside`, with Own text, a radius and a box shadow, and say in TOK-56 that the whole page holds them. Then `T:741-744` fails under S2.

### Point 2: are the `colors` Tokens ordered by summed Uses? Verdict: **gap, confirmed**

The author's report is right. The code orders by the summed Uses of each Token (`K:175`: `sorted(tokens, key=lambda token: (-token.uses, key(token)))`, where `uses` is the sum of the Group, `K:224`). That is the order the Terms ask for (Family order → Rank order of the Tokens, by Uses).

But C1 keeps the Tokens in build order, which is the order their Groups were opened, and it passes all 75 tests. C2 ranks by the Representative's own Uses, and it passes all 75 too. On `tokens-groups.html` (`T:666-672`) build order and summed order are the same: `#333333` (8 Uses, opened first), then `#1a73e8` (opened with 4, ends with 7), then `#808080` (opened with 2, ends with 4), then the two of 1 Use. No Group's sum overtakes a Representative opened before it. On `tokens-page.html` and `tokens-limit.html` no two colours are Near, so the two orders cannot differ.

The Limit is not held either: a cut in build order keeps different Tokens only when the two orders differ.

**Fix**: a criterion and fixture rows where they differ. For example, add five boxes of one colour Near no other to `tokens-groups.html`. In build order that colour (5) comes before `#1a73e8` (opened with 4). In summed order `#1a73e8` (7) comes first. Both C1 and C2 then die on the whole-list assertion `T:666`.

### Point 3: are the error criteria anchored to the spec or to the SDK prefix? Verdict: **anchored to the spec; minor spec-precision gap, not blocking**

The SDK wraps every `ToolError` as `Error executing tool <name>: <message>` (`.venv/Lib/site-packages/mcp/server/mcpserver/tools/base.py:210`). `fail` (`T:51-61`) first asserts that the text starts with that prefix. It then compares the rest whole, with `==`, against the spec's literal text for TOK-57 (`T:749`), TOK-58 (`T:753`), TOK-69 (`T:853`) and TOK-71 (`T:872`), and with `startswith` for TOK-70 (`T:860`), as that criterion asks. So the asserted value is the spec's text, character for character. That is stricter than the earlier tools' tests, which use a substring `in` (`tests/test_inspect_element.py:444`).

The prefix assertion also discriminates. A crash reaches the client as `Error executing tool extract_tokens` with no message (`base.py:213`). Mutant E2 (a `ValueError` instead of a `ToolError`) is killed by `T:747` through that very prefix check.

The gap: the spec says "the call SHALL fail with the message X" but never says what "the message" is in the result the client receives. The client's text block is the SDK prefix followed by X, not X. The test settles this by an assumption about the SDK that is written in a test comment (`T:58`), not in the spec. If the SDK changed its prefix, the tests would fail while the tool still meets the spec.

**Fix (spec wording only)**: add a Term, "Message: the text of the error's one text block after the SDK's `Error executing tool extract_tokens: `", or write it into the Assumptions table. No code or test change is needed.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ `tokens.py` is the Terms as code; one grouping walk (`K:134-153`) is shared by every Family that groups |
| Surgical changes | ✅ Earlier tests change only in the two tool lists (TOK-77) |
| No scope creep | ✅ |
| Matches patterns | ✅ Same timeout, `ToolError` and `CallToolResult` shape as the other tools |
| Spec-anchored outcome check | ✅ (2 flags above) |
| Per-layer Coverage Expectation met | ✅ 1:1 through the MCP boundary; ΔE2000 alone below it, as the Assumptions allow |
| Every test maps to a spec requirement | ✅ Each test carries the criterion it holds; `T:780` (TOK-24 per element) and the whole-list tests `T:471` and `T:657` hold the L-020 order |
| Documented guidelines followed | ✅ `CONTRIBUTING.md`, `docs/SPEC.md` Testing Decisions (one seam) |

---

## Edge Cases

- [x] TOK-78: two Near Values on one element are two Uses (`T:691-696`)
- [x] TOK-79: the browser's default `body` margin is counted (`T:699-703`)
- [x] A scope that matches nothing (TOK-57), is not a selector (TOK-58), or matches only elements that are not Read (TOK-59)
- [ ] A Family with no Value in the scope (TOK-56): asserted, but not told apart from the whole page (point 1)

---

## Gate Check

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_color.py tests/test_extract_tokens.py`, run by the Verifier on the real tree at `e3fcf12`
- **Result**: pyright 0 errors; ruff check passed; ruff format check passed (120 files); **75 passed**, 0 failed, 0 skipped, in 81.04s. Exit 0.
- **Test count before feature**: 421 collected at `486004c` (`tasks.md`)
- **Test count after feature**: 496 collected (Build at `1c1b55f`, 496 passed, recorded under T29; not re-run by the Verifier, by the orchestrator's instruction)
- **Delta**: +75 (`test_color.py` 1, `test_extract_tokens.py` 74); none deleted
- **Skipped tests**: none
- **Failures**: none
- **Linux**: 75 passed (T28, recorded; not re-run)

---

## Fix Plans

### Fix 1: hold the scope for typography, radii and shadows (S2; TOK-56)

- **Root cause**: the fixture of TOK-56 has no non-colour Value outside the scope, so an empty Family proves nothing.
- **Fix task**: Spec (maintainer): TOK-56, or a new criterion, gives `tokens-scope.html` an element outside the cards with Own text, a radius and a box shadow, and says the whole page holds them while `#one-child` does not. Tests: extend `T:741-744`, or add a whole-page check of those Families. Done when S2 fails in a scratch copy. `src/` is unchanged.
- **Priority**: Major

### Fix 2: hold the Family order of `colors` by summed Uses (C1, C2)

- **Root cause**: no fixture has a Group whose summed Uses pass a Representative opened before it.
- **Fix task**: Spec (maintainer): a criterion on `tokens-groups.html` with, for example, five boxes of one colour Near no other, and the whole `colors` list in order (TOK-41's Token before it). Test: the whole list at `T:666`. Done when C1 and C2 fail in a scratch copy.
- **Priority**: Major

### Fix 3: hold the box clause of Painted text (P1)

- **Root cause**: no criterion has an element with Own text that paints no box inside a box that does. Terms: "when at least one of them paints a box".
- **Fix task**: Spec (maintainer): a criterion on `tokens-used.html`, for example a 100x20 box whose Own text paints no box, with a font family, size, colour and text shadow no other element has, none of them held. The Verifier did not probe which CSS makes the text paint no box in Chromium 153 (`font-size: 0` is one candidate), so Design should confirm it. Done when P1 fails in a scratch copy.
- **Priority**: Minor (it is a rare page, but the rule is in the Terms)

### Fix 4 (wording, non-blocking): define "message"

- **Fix task**: add to the spec's Terms or Assumptions what "the message" of a failure is: the text after the SDK's `Error executing tool extract_tokens: `.
- **Priority**: Cosmetic

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| TOK-01 to TOK-55, TOK-57 to TOK-79 | Implemented | ✅ Verified (TOK-01 and TOK-52 assertions hold; the order rule behind them is Fix 2) |
| TOK-56 | Implemented | ❌ Needs Fix (Fix 1) |

The spec was not edited: the Verifier writes only this file.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 79/79 criteria have an assertion on the spec's outcome; 2 spec-precision gaps flagged (TOK-56; "message").
**Sensor**: 18/22 mutations killed; S2, C1, C2 and P1 survived.
**Gate**: 75 passed, 0 failed (Full).

**What works**: every value, Role, Use, variant and order the criteria name; the ΔE2000 function against the 34 published pairs; scope, matches under matches and open shadow trees; the Limit; the summary; the contract and the errors. 18 mutants across grouping, rank, reading, counting, scoping, the Limit and errors are killed.

**Issues found**: three rules of the Terms are built but not held by any fixture: the scope for typography, radii and shadows; the `colors` order by summed Uses; the box clause of Painted text. All three are fixed in the spec and its fixtures; `src/` should not need to change.

**Next steps**: the maintainer decides the spec rows for Fixes 1 to 3 (and the wording of Fix 4). A fix round adds the fixtures and tests, then the Verifier runs again, re-running S2, C1, C2 and P1.
