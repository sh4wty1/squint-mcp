# Pixel budget per Capture checks

Profile: light
Plan: `.specs/features/capture-pixel-budget/plan.md`

15 checks in 4 slices · 3 one-way doors · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. Where `uv` is not on the path, `uv run <tool>` is `.venv/bin/<tool>`. Feature base: `f2c6213`.

## Checks

### S1 - the texts of a Capture share one budget · 5 files · 38 KB · ~10k

**C1** - `detect_visual_bugs` with `low-contrast-real` on `pixel-budget.html` with `#texts` targeted (55 texts of 1440x180 over 1440x10000 of noise, each reported) succeeds and takes less than 10s longer than on the same page without them (AC 1, door 2)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_many_texts_over_millions_of_colours_add_little_to_the_call" -v`

**C2** - On a page whose texts cover 262,144 pixels or fewer together, a text is still judged on exactly a tenth of its pixels: the bounds fixture (57,000 text pixels) reports the tenth at the right edge and not the part under a tenth at the left edge (AC 2)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_a_tenth_of_the_text_at_its_right_edge_is_enough" -v`
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_under_a_tenth_of_the_text_at_its_left_edge_is_not_reported" -v`

**C3** - `#small` (100x40, `#999999` on white) on `pixel-budget.html` with `#texts` targeted is reported with `contrastRatio == 2.84` and `sampledBackground == "#ffffff"` (AC 3, AC 4, door 1)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_a_small_text_among_many_large_ones_keeps_its_ratio" -v`

**C4** - `#big-text` of `pixel-cost.html` (600x600, a light band behind its last fifth) with `#over-noise` targeted (another text, of 6,220,800 pixels) is reported with `contrastRatio == 1.6` and `sampledBackground == "#cccccc"` (AC 5, door 1)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_a_text_over_the_limit_next_to_another_is_still_judged_on_its_worst_part" -v`

**C5** - Two calls of `detect_visual_bugs` on `pixel-budget.html` with `#texts` targeted return the same structured content (AC 6)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_the_same_call_on_many_texts_returns_the_same_content" -v`

**C6** - Every test of `low-contrast-real` that exists at `f2c6213` passes unedited (AC 7)
Proof: `uv run pytest tests/test_low_contrast_real.py -v`
Proof: `git diff f2c6213..HEAD -- tests/test_low_contrast_real.py | grep -c "^-[^-]"` prints `0`

### S2 - a sampled region keeps the colours of a fine pattern · 4 files · 34 KB · ~9k

**C7** - `inspect_element` on `#rows`, `#columns` and `#checker` of `sampled-patterns.html` (1024x1024 each, red and blue at a 1px period) reports exactly `#ff0000` and `#0000ff`, each with a share from 0.4 to 0.6 (AC 8, door 3)
Proof: `uv run pytest "tests/test_inspect_element.py::test_a_sampled_pattern_keeps_both_its_colours" -v` runs 3 cases

**C8** - `inspect_element` on `#halves` of `pixel-cost.html` reports exactly `#ff0000` and `#0000ff`, with shares within 0.01 of 0.499 and 0.501 (AC 9)
Proof: `uv run pytest "tests/test_inspect_element.py::test_a_region_over_the_limit_keeps_its_painted_colours_and_shares" -v`

**C9** - `#text-dark-first` and `#text-light-first` of `sampled-patterns.html` (white text of 600x600 over 1px rows of black and `#cccccc`, starting with one and with the other) are each reported with `contrastRatio == 1.6` and `sampledBackground == "#cccccc"` (AC 10, door 3)
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_text_over_one_pixel_rows_is_judged_on_both_colours" -v` runs 2 cases

**C10** - Two calls of `inspect_element` on `#rows` return the same `sampledColors` (AC 11)
Proof: `uv run pytest "tests/test_inspect_element.py::test_a_sampled_pattern_is_the_same_on_every_call" -v`

**C11** - A region of 262,144 pixels or fewer still reports the shares of all its pixels, with the existing tests unedited (AC 12)
Proof: `uv run pytest "tests/test_inspect_element.py::test_sampled_colors_are_the_painted_colors_by_share" -v`
Proof: `uv run pytest "tests/test_inspect_element.py::test_sampled_colors_keep_the_three_most_frequent" -v`

### S3 - the record · 3 files · 13 KB · ~3k

**C12** - `CHANGELOG.md` has an entry under `[Unreleased]`, above `## [0.1.0]`, that names the 262,144 pixels across the texts of a page and the 1px or 2px pattern (AC 13)
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | grep -c "262,144"` prints `1` or more
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | grep -c "pattern"` prints `1` or more

**C13** - The `# Source:` comment of `COLOR_COUNT_MAX_PIXELS` in `config.py` says that for text the limit is per Capture (AC 14)
Proof: `grep -B8 "^COLOR_COUNT_MAX_PIXELS" src/squint_mcp/config.py | grep -c "Capture"` prints `1` or more

**C14** - `vision.py` no longer points at #11 (AC 15)
Proof: `grep -c "#11" src/squint_mcp/vision.py` prints `0`

### S4 - gate

**C15** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| one-way doors (3) | door 1, the cap C3 · door 2, the budget C1 · door 3, the jitter C7 | - |
| 1px patterns (3) | `rows` C7 · `columns` C7 · `checker` C7 | - |
| first row behind the text (2) | `dark-first` C9 · `light-first` C9 | - |
| callers of the sampling (2) | `sample_colors` C7 · `text_backgrounds` C9 | - |
| texts against the budget (3) | all under it together C2 · one under the cap among larger ones C3 · one over the cap C4 | - |

- No check names a status code, a route or a response shape: no tool, field or error changes
- C7 and C9 are table-driven over their sets, sizes 3 and 2

## Swept

- validation: n/a - no input surface changes; the budget is a constant, not a parameter
- failure modes: existing - a text with no pixels, or no text pixel in its sample, yields nothing: `tests/test_low_contrast_real.py::test_text_without_a_box_is_not_reported`; a sampled side never rounds down to 0 (`max(1, ...)`)
- idempotency: C5, C10
- authorization: n/a - a local stdio server, no caller to tell apart
- concurrency: C1 - the work stays synchronous on the event loop; bounded per Capture, it holds the loop for a second instead of a minute
- data lifecycle: n/a - nothing is retained between calls
- dependency failure: n/a - no new dependency; the sampling is Pillow and the standard library
- state transitions: n/a - the Check holds no state; the cap is derived from the Capture on each call
- observability: n/a - no log requirement; a field saying that a result was sampled is out of scope in the plan

## Handoff

- S1-S3 = 85 KB of reading, ~22k tokens, one surface (`vision.py` and the Check that calls it), under the 150k budget - one builder
