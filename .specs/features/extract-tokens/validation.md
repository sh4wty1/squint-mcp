# extract-tokens Validation

**Date**: 2026-10-15
**Spec**: `.specs/features/extract-tokens/spec.md` (TOK-01 to TOK-81; TOK-56 rewritten, TOK-80 and TOK-81 new, the Term **Message** added)
**Diff range**: the surface of the feature is `ee2c88e..07d6c2c` (branch `feat/extract-tokens`; `origin/main` is `4e0be46`, the local `main` is stale and was not used). The fix round is `840099a..07d6c2c` (5 commits, `3c3d41c` to `07d6c2c`): it touches `.specs/features/extract-tokens/spec.md`, `tasks.md`, `tests/test_extract_tokens.py` and the fixtures `tokens-groups.html`, `tokens-scope.html` and `tokens-used.html`. `git diff --stat 840099a..07d6c2c -- src` is empty: `src/` is unchanged by the fix round.
**Verifier**: independent sub-agent (author ≠ verifier), second pass

**Verdict**: ✅ PASS

**Result**: ✅ PASS

All 81 criteria have an assertion at `file:line` on the outcome the spec gives. The Full gate is green on the real tree (77 passed). The discrimination sensor injected 12 behaviour-level mutants, among them the four survivors of the first pass (S2, C1, C2, P1), each re-implemented from the first pass's description: all 12 were killed. The two spec-precision gaps of the first pass are closed: TOK-56 now has a fixture where the whole page differs from the scope, and the Term **Message** (`spec.md:43`) says what "the message" of a failing call is.

Abbreviations: `T` = `tests/test_extract_tokens.py`, `K` = `src/squint_mcp/tokens.py`, `X` = `src/squint_mcp/tools/extract_tokens.py`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T29 | ✅ Done | Checked by the first pass; `src/` has not changed since (`840099a..07d6c2c`). |
| T31 | ✅ Done | `#outside` of `tokens-scope.html` gains its text, font, radius and shadow; TOK-56's test reads the whole page first (`T:771-780`). |
| T32 | ✅ Done | `#c1` to `#c5` of `#ff8800` in `tokens-groups.html`; TOK-80's test (`T:604-615`); the row of `#ff8800` in the whole-list test (`T:696`). |
| T33 | ✅ Done | `#mute` in `tokens-used.html`; TOK-81's test (`T:334-343`); TOK-24's count 31 to 32 (`T:480`). |
| T34 | ✅ Done | The Term **Message** (`spec.md:43`); no test or code changed. |
| T30 | ⏳ Pending | Waits for this PASS, by design. Not counted as a gap. |

---

## Spec-Anchored Acceptance Criteria

The `extract` helper (`T:39-48`) runs on every successful call: it asserts `is_error is False`, then `assert_sums_hold` (`T:64-81`, TOK-13 and TOK-14), then at most 20 Tokens per Family (`T:46-47`, TOK-66). The `fail` helper (`T:51-61`) asserts `is_error is True`, `structured_content is None` and one text block (TOK-72), asserts that the text starts with `Error executing tool extract_tokens: ` and returns the rest. That rest is exactly the **Message** of the spec's new Term (`spec.md:43`); the SDK writes that prefix at `.venv/Lib/site-packages/mcp/server/mcpserver/tools/base.py:210`.

### P1: Read the tokens of a page

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-01 | 5 colour tuples, whole and in order | `T:187` `rows(colors, *fields) == [("#333333",3,3,0,0), …]`; `T:195` one variant each | ✅ PASS |
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
| TOK-15 | `#aa0000` uses 1, text 1 | `T:276-277` | ✅ PASS |
| TOK-16 | `#222222` text 1; no `#111111` | `T:282-283` | ✅ PASS |
| TOK-17 | no value starting `#008080` | `T:288` (Tokens and variants) | ✅ PASS |
| TOK-18 | no `#445566…`, no 8-digit `…00` | `T:293-294` | ✅ PASS |
| TOK-19 | `#00000080`, background 1 | `T:302` | ✅ PASS |
| TOK-20 | `#0000aa` uses 1, border 1; no `#00aa00` | `T:310`, `T:312` | ✅ PASS |
| TOK-21 | four border Tokens, border 1 each | `T:317-318` | ✅ PASS |
| TOK-22 | no `#aa00aa` | `T:463` | ✅ PASS |
| TOK-23 | no `#00aaaa` | `T:469` | ✅ PASS |
| TOK-24 | none of the 3 colours; none of the 3 elements counted | `T:476-477`; `T:480` `result["elements"] == 32`; `T:822-823` (each alone gives 0) | ✅ PASS. Re-derived: the `body` of `tokens-used.html` holds 36 elements, all with an `id`; minus `#none`, `#flat-w`, `#flat-h`, `#hidden`, `#faded`, `#faded-child` that is 30, plus `html` and `body`: 32. `#mute` (100x20, visible) is Read, as TOK-81 says. |
| TOK-25 | no 40/900/50/Georgia in any typography list; sizes holds 12 | `T:351-354` | ✅ PASS |
| TOK-26 | sizes holds 13; line-height uses = size uses − 1 | `T:360-364` | ✅ PASS |
| TOK-27 | lineHeights holds 30 | `T:372` | ✅ PASS |
| TOK-28 | 51/53/55/57, uses 1, margin 1 | `T:377-379` | ✅ PASS |
| TOK-29 | 61/63/65/67, uses 1, padding 1 | `T:384-386` | ✅ PASS |
| TOK-30 | no 620 | `T:393` | ✅ PASS |
| TOK-31 | nothing ≤ 0; no 71 | `T:398-399` | ✅ PASS |
| TOK-32 | 81, 83 with gap 1 | `T:404-405` | ✅ PASS |
| TOK-33 | 85/87/89, uses 1, gap 1 | `T:413-415` | ✅ PASS |
| TOK-34 | no 91 | `T:420` | ✅ PASS |
| TOK-35 | 41/43/45/47px, uses 1; no `0px` | `T:427-430` | ✅ PASS |
| TOK-36 | `50%`, `10px 20px` uses 1, after every px Length | `T:439` (last two rows); `T:542-549` (whole list) | ✅ PASS |
| TOK-37 | `(text, rgb(0, 0, 0) 1px 1px 2px)` uses 1 | `T:448` (every `text` row) | ✅ PASS |
| TOK-38 | one box Token of the two-layer text, uses 1 | `T:456` (every `box` row) | ✅ PASS |
| TOK-39 | holds `#336699` | `T:324` (a Token `value`) | ✅ PASS |
| TOK-40 | holds `#ff0000` | `T:331` | ✅ PASS |
| TOK-81 (new) | no typography list holds `0`, `700`, `37`, `Courier, monospace`; `colors` does not hold `#abcdef`; no Value of `shadows` holds `3px 3px 3px` | `T:338-340` `value not in values(typography[name])` for each of the 4 lists and 4 values; `T:341` `"#abcdef" not in values(result["colors"])`; `T:342-343` `"3px 3px 3px" not in value` for every Value of `shadows` | ✅ PASS. `values()` (`T:118-125`) reads Tokens and variants, as "does not hold" is defined (`spec.md:157`). The fixture matches the criterion: `tests/fixtures/tokens-used.html:190-196` (`#mute`, 100x20, `font: 700 0px/37px Courier, monospace`, `color: #abcdef`, `text-shadow: 3px 3px 3px #abcdef`). The whole lists of the page (`T:491-553`) did not change, so the values are absent, not merely moved. |

### P1: Fold values that are nearly equal

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-41 | `#1a73e8` uses 7, roles {1,6,0}, variants `(#1a73e8,4),(#1a78e8,3)` | `T:562-568` | ✅ PASS |
| TOK-42 | `#1a79e8` uses 1, single variant | `T:577-579` | ✅ PASS |
| TOK-43 | `#1a73e880` uses 1, apart from `#1a73e8` | `T:585-587` | ✅ PASS |
| TOK-44 | `#808080` uses 4, variants `(#808080,2),(#858585,2)` | `T:596-601` | ✅ PASS |
| TOK-45 | `(15,1),(16,4),(17,4)` | `T:621` | ✅ PASS |
| TOK-46 | variants of 17: `(17,2),(16.75,1),(17.75,1)` | `T:629-633` | ✅ PASS |
| TOK-47 | variants of 16: `(16,3),(16.5,1)` | `T:642-645` | ✅ PASS |
| TOK-48 | `8` uses 3, padding 3, variants `(8,2),(8.5,1)` | `T:660-662` | ✅ PASS |
| TOK-49 | `4px` uses 3, variants `(4px,2),(4.5px,1)` | `T:667-672` | ✅ PASS |
| TOK-50 | one Token `20`, variants end `(20.5,1)` | `T:678-680` | ✅ PASS |
| TOK-51 | four Tokens of uses 1 | `T:652-655` | ✅ PASS |
| TOK-80 (new) | `(#333333,8),(#1a73e8,7),(#ff8800,5),(#808080,4),(#1a73e880,1),(#1a79e8,1)`, whole and in order | `T:608-615` `rows(colors, "value", "uses") == [...]`; `T:693-700` the same list with Roles (`("#ff8800", 5, 0, 5, 0)`) | ✅ PASS. Re-derived: in Rank order of Values `#ff8800` (5) comes before `#1a73e8` (4 alone), so its Group opens first; the order the spec asks for exists only by the summed Uses (7). The Verifier recomputed with the shipped `lab_of` and `delta_e_2000`: the smallest ΔE2000 from `#ff8800` to another colour of the page is 31.6362 (`#858585`), so it is Near none. Fixture: `tests/fixtures/tokens-groups.html:61-69`, `:168-172`. |

### P1: Narrow the reading to a part of the page

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-52 | 4 colour rows in order; scope `.card` | `T:740-746` | ✅ PASS |
| TOK-53 | elements 6 | `T:752` | ✅ PASS |
| TOK-54 | holds `#ff0000`; elements 9 | `T:758-760` | ✅ PASS (`values()` also accepts a variant; equivalent here, no two colours of the page are Near) |
| TOK-55 | `(#00ffff,1)` alone; elements 1 | `T:765-766` | ✅ PASS |
| TOK-56 (rewritten) | without `scope`: six Families each one Token, those of `#outside`; with `#one-child`: every Family but `colors` `{total: 0, tokens: []}` | `T:773-780` six `rows(...) == [single row]` assertions, whole lists, with the spec's exact values (`("box", "rgba(0, 0, 0, 0.5) 0px 2px 4px 0px", 1)` at `T:778-779`); `T:782-783` `family == {"total": 0, "tokens": []}` for `families(result)[1:]` | ✅ PASS. The first pass's spec-precision gap is closed: the fixture (`tests/fixtures/tokens-scope.html:23-29`, `:47`) now gives the whole page a non-colour Value in each of the six Families, so the empty Families of `#one-child` are told from the whole page. Mutants S2 to S5 die at `T:783`. |
| TOK-57 | Message `Scope ".missing" matched no elements.` | `T:787-788` `message == …` | ✅ PASS (Message per `spec.md:43`) |
| TOK-58 | Message `Invalid selector "div[".` | `T:792` `== 'Invalid selector "div[".'` | ✅ PASS (Message per `spec.md:43`) |
| TOK-59 | elements 0; every Family empty | `T:799-802` | ✅ PASS; now also told from the whole page by `#outside` (S2 to S5 die at `T:802`) |
| TOK-60 | exact zero summary | `T:808` | ✅ PASS; S2 to S5 die here too |
| TOK-61 | fails; not a whole-page reading | `T:815-816` (fails through `fail`, and the message is not a summary) | ✅ PASS (the spec gives no message, and none is asserted) |

### P2: Bound the response

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-62 | total 21; 10…190, then 210 | `T:832-833` | ✅ PASS |
| TOK-63 | total 20; 10…200 | `T:838-839` | ✅ PASS |
| TOK-64 | total 21; first 20 by text, in order | `T:847-869` (exact list) | ✅ PASS |
| TOK-65 | the text says `colors 21` and `spacing 21` | `T:876-877` | ✅ PASS |
| TOK-66 | ≤ 20 per Family | `T:46-47`, on every `extract` call | ✅ PASS |

### P2: Tool contract, config and documents

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-67 | hints, output schema, `url` required, `scope` optional string, viewport min 1 | `T:131-158` | ✅ PASS |
| TOK-68 | holds `#111111`, not `#999999`; viewport 375x812 | `T:886-888` | ✅ PASS |
| TOK-69 | Message `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `T:892-894` `==` | ✅ PASS (Message per `spec.md:43`) |
| TOK-70 | Message starts with `Could not load ` + url | `T:899` `.startswith(f"Could not load {url}")` | ✅ PASS (Message per `spec.md:43`) |
| TOK-71 | Message `Timed out after 30s.` | `T:911` `message == "Timed out after 1s."` with `TOTAL_TIMEOUT_S` set to 1.0 (`T:907`); the 30 is `src/squint_mcp/config.py:8`, formatted by `X:68` (`{:g}s`) | ✅ PASS (mutant E3 on the format dies at `T:911`) |
| TOK-72 | error, no structured content | `T:55-56`, in every `fail` call | ✅ PASS |
| TOK-73 | stabilized false; the text ends `; not stabilized.` | `T:922-924` | ✅ PASS |
| TOK-74 | 34 published pairs to four places | `tests/test_color.py:18` (34 rows), `tests/test_color.py:21-22` (both orders) | ✅ PASS |
| TOK-75 | three named constants, each with its source | `src/squint_mcp/config.py:191-205` (read) | ✅ PASS |
| TOK-76 | README describes the tool; CHANGELOG under Unreleased | `README.md:44`, `README.md:48`; `CHANGELOG.md:7`, `CHANGELOG.md:11` (read) | ✅ PASS |
| TOK-77 | earlier tests pass, with only the two tool lists changed | `git diff ee2c88e..07d6c2c` on earlier tests: only `tests/test_ping.py` and `tests/test_inspect_element.py` gain `extract_tokens` (and the ping test's name). Build 498 passed at `496676d`, recorded under T34 (not re-run here, by the orchestrator's instruction) | ✅ PASS |

### Edge Cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| TOK-78 | `40` uses 2, variants `(40,1),(40.5,1)` | `T:722-724` | ✅ PASS |
| TOK-79 | `8` uses 1, margin 1 | `T:730-731` | ✅ PASS |

**Status**: ✅ All 81 criteria are covered, each assertion on the spec's outcome. 0 spec-precision gaps: TOK-56's is closed by its new fixture, and that of "the message" (TOK-57, 58, 69, 70, 71) by the Term **Message**, which the `fail` helper (`T:59-61`) implements to the character.

---

## Discrimination Sensor

**Depth**: expanded (12 mutants): the four survivors of the first pass, re-implemented from its descriptions, and eight more aimed at the new or changed criteria (TOK-56, TOK-80, TOK-81, TOK-24, TOK-71).

**Isolation**: for each mutant a fresh copy of `src/squint_mcp` in `C:\Users\Dev\AppData\Local\Temp\tok-verify2\<name>\squint_mcp`, the mutation applied by exact string replacement (asserted to occur once), then `uv run pytest tests/test_color.py tests/test_extract_tokens.py -q --tb=line -p no:cacheprovider` from the repo root with `PYTHONPATH` set to the copy's parent and `PYTHONDONTWRITEBYTECODE=1`. Before each run `squint_mcp.__file__` was asserted to resolve into the copy (e.g. `C:\Users\Dev\AppData\Local\Temp\tok-verify2\S2\squint_mcp\__init__.py`). An unmutated copy (BASE) passed 77 of 77 first. Each copy was deleted after its run, and the scratch directory at the end. No `git stash`, no worktree, no edit of the real `src/`. `git status --porcelain` of the real tree was empty before and empty after (byte-identical, `cmp`), and HEAD stayed at `07d6c2c`. Every mutant ran the whole Quick gate (77 tests), not a `-k` subset.

| # | File:line | Description | Killed? | Killed by |
| - | --------- | ----------- | ------- | --------- |
| S2 | `X:71-72` | With a scope, a second Capture of `*` (whole page, no descendants); its `typography`, `radii` and `shadows` replace those of the scope; `spacing` and `colors` stay scoped | ✅ Killed (survived in pass 1) | `T:783` (TOK-56), `T:802` (TOK-59), `T:808` (TOK-60) |
| C1 | `K:233` | `colors` Tokens kept in build order (the order their Groups were opened), then cut at the Limit | ✅ Killed (survived in pass 1) | `T:608` (TOK-80), `T:693` (TOK-80 / whole list) |
| C2 | `K:233` | `colors` Tokens ranked by the Uses of their Representative (first variant), then by value, then cut at the Limit | ✅ Killed (survived in pass 1) | `T:608` (TOK-80), `T:693` |
| P1 | `K:265` | Painted text = Own text, whether or not it paints a box (`return element.own_text`) | ✅ Killed (survived in pass 1) | `T:340` (TOK-81, `Courier, monospace` in `families`), `T:448` (TOK-37), `T:491` (whole list of `tokens-used.html`) |
| S3 | `X:71-72` | As S2, but only `shadows` read from the whole page | ✅ Killed | `T:783`, `T:802`, `T:808` |
| S4 | `X:71-72` | As S2, but only `radii` read from the whole page | ✅ Killed | `T:783`, `T:802`, `T:808` |
| S5 | `X:71-72` | As S2, but only `typography` read from the whole page | ✅ Killed | `T:783`, `T:802`, `T:808` |
| P6 | `K:206` | The text colour alone ignores the box clause (`if element.own_text:` in `_colors`) | ✅ Killed | `T:341` (TOK-81, `#abcdef`), `T:491` |
| P7 | `K:415` | The text shadow alone ignores the box clause (`if element.own_text:` in `_shadows`) | ✅ Killed | `T:343` (TOK-81, `3px 3px 3px`), `T:448`, `T:550` |
| C3 | `K:233` | `colors` kept in Family order by value (`by_value=True`), not in Rank order | ✅ Killed | `T:187` (TOK-01), `T:491`, `T:608`, `T:693`, `T:740` (TOK-52) |
| R2 | `K:255-260` | A Read element also needs its Own text, if any, to paint a box (`#mute` no longer Read) | ✅ Killed | `T:480` (TOK-24, `31 == 32`) |
| E3 | `X:68` | The timeout Message formatted with `{}` instead of `{:g}` (`1.0s`) | ✅ Killed | `T:911` (TOK-71) |

**Sensor depth**: expanded
**Result**: 12/12 killed - ✅ PASS

The 18 mutants killed in the first pass (S1, G1 to G6, R1, U1, P2 to P5, L1, E1, E2, D1, X1) were not re-run: `src/` is unchanged since, and the fix round only added fixture rows and assertions, none removed (76 tests in the module, 74 before plus TOK-80 and TOK-81). The fix round only added rows and assertions to existing tests (`T:696`, `T:770-780`), with one exception: `T:480` (TOK-24), whose count rose from 31 to 32 with `#mute`. R2 shows that count still discriminates.

---

## The changes of the fix round, checked

- **TOK-56 / S2**: the criterion now names the whole page's six Tokens, and the test asserts each list whole (`T:773-780`) before the empty Families of `#one-child` (`T:782-783`). The fixture matches the spec's preamble (`spec.md:222`): `#outside` has the Own text `Out`, `font: 400 12px/16px Arial, sans-serif`, `color: #000000`, `border-radius: 6px` and `box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5)`; no other element has text, a radius or a shadow. TOK-52 to TOK-55 and TOK-57 to TOK-60 still pass with their assertions unchanged (`git diff 840099a..07d6c2c -- tests/test_extract_tokens.py` touches none of them).
- **TOK-80 / C1, C2**: the five boxes of `#ff8800` make the build order (and the Representative's order) differ from the summed order. The whole-list test of the page (`T:693-700`) gained only the row of `#ff8800`; the other Families of that test are unchanged.
- **TOK-81 / P1**: one 100x20 element whose text, of `font-size: 0`, paints no box. The task notes a Chromium 153 probe: one 0x0 rect. That the rule now discriminates is shown by P1, P6 and P7, each killed at its own clause of `T:338-343`.
- **Message**: `spec.md:43`. The `fail` helper already compared the text after that prefix. TOK-57, 58, 69 and 71 compare it whole with `==`, and TOK-70 with `startswith`, as the criterion asks.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ No code changed in the fix round; the fixes are fixture rows and assertions |
| Surgical changes | ✅ `840099a..07d6c2c` touches only `.specs/`, `tests/test_extract_tokens.py` and three fixtures |
| No scope creep | ✅ |
| Matches patterns | ✅ The new tests use the module's `extract`, `rows` and `values` helpers |
| Spec-anchored outcome check (asserted values match spec) | ✅ 81/81 |
| Per-layer Coverage Expectation met | ✅ 1:1 through the MCP boundary; ΔE2000 alone below it, as the Assumptions allow |
| Every test maps to a spec requirement | ✅ The two new tests hold TOK-80 (`T:604`) and TOK-81 (`T:334`) |
| Documented guidelines followed | ✅ `CONTRIBUTING.md`, `docs/SPEC.md` Testing Decisions (one seam) |

---

## Edge Cases

- [x] TOK-78: two Near Values on one element are two Uses (`T:719-724`)
- [x] TOK-79: the browser's default `body` margin is counted (`T:727-731`)
- [x] A scope that matches nothing (TOK-57), is not a selector (TOK-58), or matches only elements that are not Read (TOK-59, now told from the whole page)
- [x] A Family with no Value in the scope (TOK-56): told from the whole page by `#outside`
- [x] Own text that paints no box in a box that does (TOK-81)

---

## Gate Check

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_color.py tests/test_extract_tokens.py`, run by the Verifier on the real tree at `07d6c2c`
- **Outcome**: pyright 0 errors, 0 warnings; ruff check `All checks passed!`; ruff format check `121 files already formatted`; **77 passed**, 0 failed, 0 skipped, in 74.90s. Exit 0.
- **Build** (recorded, not re-run, by the orchestrator's instruction): 498 passed at `496676d`, pyright 0 errors, ruff clean (T34)
- **Linux** (recorded, not re-run): 77 passed in 73.84s, Playwright Docker image (T28)
- **Test count before feature**: 421 collected at `486004c` (`tasks.md`)
- **Test count after feature**: 498 (Build); the two modules hold 77 (`test_color.py` 1, `test_extract_tokens.py` 76)
- **Delta**: +77; +2 since the first pass (TOK-80, TOK-81); none deleted, none weakened (the one changed assertion, `T:480`, is a count that rose with the new element)
- **Skipped tests**: none
- **Failures**: none

---

## Fix Plans

None. The four fix plans of the first pass are done (T31 to T34) and verified above.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| TOK-01 to TOK-55, TOK-57 to TOK-79 | Implemented | ✅ Verified |
| TOK-56 | Implemented (❌ Needs Fix in pass 1) | ✅ Verified |
| TOK-80 | Implemented | ✅ Verified |
| TOK-81 | Implemented | ✅ Verified |

The spec was not edited: the Verifier writes only this file. T30 updates the Status column.

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 81/81 criteria matched to the spec's outcome; 0 spec-precision gaps.
**Sensor**: 12/12 mutations killed, among them S2, C1, C2 and P1, the four survivors of the first pass.
**Gate**: 77 passed, 0 failed (Full, run by the Verifier); Build 498 and Linux 77 as recorded.

**What works**: every value, Role, Use, variant and order the criteria name; the scope now held for every Family; the order of `colors` by the Uses of a whole Group; the box clause of Painted text, held for type, text colour and text shadow separately; the Messages of the failures as the new Term defines them.

**Issues found**: none.

**Next steps**: T30 (mark slice 10 as done), then the maintainer's go-ahead for a push and a pull request.
