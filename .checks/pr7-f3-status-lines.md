# PR #7 F3: status lines

Profile: light (none declared in `AGENTS.md`).

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/7#pullrequestreview-5449173369 - F3, still open in round 2, with its four items
- `.specs/features/detect-visual-bugs-text-clipped/validation.md` - "For the maintainer", option (a): accept the feature on a re-run of M1, M4, M5 and M6 alone
- `.specs/features/detect-visual-bugs-text-clipped/spec.md:284` - DVB-68: on a PASS, `docs/ROADMAP.md` shows slice 3 as `concluída` in the table and in its section
- conversation - the maintainer asked for F3 to be resolved, which takes option (a)

## Out of scope

- Any change under `src/` or `tests/` - Fix 16 to Fix 19 are already applied by `6ffb1c7` and `ea482ef`
- A fourth full validation pass - option (a) asks for the four mutants alone
- Text cut inside an inline child of a parent whose own text fits - a decision for the maintainer, not a status line
- `design.md`, `tasks.md`
- Merging PR #7

## Landing

Touches `docs/ROADMAP.md` (table row and section of slice 3), `.specs/STATE.md` (Handoff), `validation.md` (verdict and the rows that carry it, one new section), and the description of PR #7. No code.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Where the re-run is recorded | A section `## Re-run of the survivors of pass 3` in `validation.md`; the body of pass 3 stays as written | Rewriting pass 3 as if it had passed - erases what the Verifier found at `9500a19` |
| M4 after `bc80575` | The mutation is applied to `_padding_right` (`text_clipped.py:57`), which now holds the expression pass 3 mutated at `:64`; it reaches the strip and the own-text comparison | Mutating only `_edge_strip` - the expression no longer lives there |

- Nothing else in this change is hard to reverse

## Checks

Mutant proofs: apply the one-line mutation to a scratch copy of `HEAD`, run the named test with `PYTHONPATH` on the mutated `src/`, expect `1 failed`; the same test passes unmutated.

### S1 - The four survivors are killed · 5 files · 30 KB · ~8k

**C1** - M1: `for name in names` becomes `for name in reversed(names)` (`src/squint_mcp/tools/detect_visual_bugs.py:73`) and the test fails
Proof: `.venv/bin/pytest "tests/test_detect_visual_bugs.py::test_the_first_unknown_check_in_the_order_given_is_the_one_named"` under the mutant

**C2** - M4: `_padding_right` returns `... + element.client_width - element.box_model.padding.right` (`src/squint_mcp/checks/text_clipped.py:57`) and the test fails
Proof: `.venv/bin/pytest "tests/test_text_clipped.py::test_the_strip_ends_at_the_padding_edge_not_at_the_content_edge"` under the mutant

**C3** - M5: `TRANSFORM_MIN_SIZE_DIFF_PX = 2` (`src/squint_mcp/config.py:70`) and the test fails
Proof: `.venv/bin/pytest "tests/test_text_clipped.py::test_an_element_painted_at_another_size_than_laid_out_is_not_reported"` under the mutant

**C4** - M6: `.replace(/[\\"]/g, "\\$&")` becomes `.replace(/"/g, "\\$&")` (`src/squint_mcp/js/collect_elements.js:20`) and the test fails
Proof: `.venv/bin/pytest "tests/test_selectors.py::test_a_backslash_in_an_attribute_value_is_escaped"` under the mutant

### S2 - The documents say what the branch holds · 3 files · 60 KB · ~15k

**C5** - `validation.md` records the re-run with one row per mutant and its verdict is PASS
Proof: `grep -c "^## Re-run of the survivors of pass 3" .specs/features/detect-visual-bugs-text-clipped/validation.md` prints 1
Proof: `grep -c "^\*\*Verdict\*\*: ✅ PASS" .specs/features/detect-visual-bugs-text-clipped/validation.md` prints 1
Proof: `grep -c "⏳" .specs/features/detect-visual-bugs-text-clipped/validation.md` prints 0

**C6** - `docs/ROADMAP.md` shows slice 3 as `concluída` in the table and in its section, and no longer says there is no code (DVB-68)
Proof: `grep -c "| 3 | .* | concluída |" docs/ROADMAP.md` prints 1
Proof: `grep -c "Status:\*\* concluída" docs/ROADMAP.md` prints 3
Proof: `grep -c "Nenhum código ainda" docs/ROADMAP.md` prints 0

**C7** - The Handoff of `.specs/STATE.md` no longer says that no production code is written, and names the merge of PR #7 as the next step
Proof: `grep -c "no production code written yet" .specs/STATE.md` prints 0
Proof: `grep -c "Next step.*PR #7" .specs/STATE.md` prints 1

### S3 - The PR description · 0 files

**C8** - The description of PR #7 no longer says the Verifier is running or "112 tests"; it gives the count of the suite at `HEAD`
Proof: `gh pr view 7 --json body --jq .body | grep -c "Still pending\|112 tests"` prints 0
Proof: `gh pr view 7 --json body --jq .body | grep -c "135 tests"` prints 1

### S4 - Gate

**C9** - Type check, lint, format and the whole suite are green at `HEAD`, 135 tests
Proof: `.venv/bin/pyright`
Proof: `.venv/bin/ruff check`
Proof: `.venv/bin/ruff format --check`
Proof: `.venv/bin/pytest`

## Swept

- validation: not in scope - no input is read
- failure modes: C1-C4 - a mutation that does not apply is reported as not applied, never as killed
- idempotency: not in scope
- authorization: C8 - editing the PR description is an outward change, asked for by the maintainer as part of F3
- concurrency: not in scope
- data lifecycle: not in scope
- dependency failure: not in scope
- state transitions: C6 - `pendente` to `concluída` only after C1-C4 hold (DVB-68)
- observability: not in scope

## Handoff

S1-S4 = ~23k of reading. One agent, no handoff.
