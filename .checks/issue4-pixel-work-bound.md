# Issue #4 - pixel work outside the total timeout

Sources:

- https://github.com/sh4wty1/squint-mcp/issues/4 - the defect (colour counting runs after the `asyncio.timeout` scope, synchronously), the measurement (15s and 42s on noise), the direction: bound the cost by reducing the region to a fixed maximum size before counting colours, rather than make the work cancellable
- conversation - the fix goes in the shared function, not in the caller; every caller of the pixel work is checked; the limit lives in `config.py` with its source; the colours sampled from the existing fixtures do not change; a `[Unreleased]` CHANGELOG entry; `README.md`, `pyproject.toml` and the `[0.1.0]` CHANGELOG section are not touched

## Callers of the pixel work

Measured on `b26d672`, on a 1440x5000 image where every pixel has its own colour:

| Function | Caller, and where it runs | Cost | In the fix |
| --- | --- | --- | --- |
| `sample_colors` | `inspect_element`, after the timeout scope | 14.5s, 12s of it sorting the counts | yes |
| `text_backgrounds` | `low-contrast-real`, run by `detect_visual_bugs` after the timeout scope | 8.8s in one box, 10-12s in 250 line boxes; the Check then sorts what it returns | yes - the same defect |
| `crop_png` | `inspect_element` once, `detect_visual_bugs` at most `MAX_CROPS` times, both after the scope | 0.02s; 0.10s at 1440x30000 in the issue | no - `thumbnail` already reduces the region to `CROP_MAX_SIDE_PX` before the PNG is encoded |
| `is_flat` | `text-clipped`, after the scope | 0.01s | no - `getcolors(maxcolors=1)` gives up at the second colour |

Through the MCP boundary, on `tests/fixtures/pixel-cost.html` before the fix: `inspect_element` on the noise takes 5s longer than on a small element of the same page (at half the height the fixture has now), and `detect_visual_bugs` with text over the noise takes 24s longer than without it.

The cost of a count grows with the distinct colours, not with the pixels: 7.2M text pixels over a flat fill or a gradient take 0.04s, over a blurred photo 0.26s, over noise 7s.

## Out of scope

- Making the pixel work cancellable, or moving it inside the `asyncio.timeout` scope - the issue chose to bound it instead; synchronous code cannot be cancelled by the scope anyway
- Moving the pixel work off the event loop - once bounded it blocks for a fraction of a second
- One budget shared by every text of a Capture - see Landing: the bound is per element
- The synchronous PNG decoding inside `capture` - inside the scope, and not what the issue measured
- `crop_png`, `is_flat` - not affected, see the table
- `README.md`, `pyproject.toml`, the `[0.1.0]` section of `CHANGELOG.md` - the release is being prepared on `feat/pypi-release`
- `git push` and the PR - asked for by the user in the request

## Landing

Touches `vision.py` (one helper that both counting functions call on their regions) and `config.py` (one limit). No caller changes: `inspect_element.py`, `detect_visual_bugs.py` and `low_contrast_real.py` stay as they are. Reuses `_region`, the `client` fixture, the `inspect`, `detect` and `findings_on` helpers and the Ahem font.

- None of this is one-way: nothing is persisted and no field, tool or parameter changes. The choices below are reversible at the cost of a refactor, and are recorded because they change what a large region reports.

| Choice | Literal shape | Alternative rejected |
| --- | --- | --- |
| How a region is reduced | `Image.resize(size, Image.Resampling.NEAREST)` to the largest size of the same aspect ratio within the limit | `thumbnail` / `reduce`, as `crop_png` does - they blend neighbours, so the counts would hold colours the page never painted, and the ink threshold of AD-004 would be applied to averaged ink |
| The limit | `COLOR_COUNT_MAX_PIXELS = 512 * 512` in `config.py`: a region of up to 262,144 pixels is counted whole | a limit on the side, like `CROP_MAX_SIDE_PX` - a 1x10000 strip would be reduced for nothing; a larger limit - every region whose colours an existing test asserts is of 100,000 pixels or fewer, so any value from there up keeps them, and this one keeps a count of noise under half a second |
| What the limit applies to in `text_backgrounds` | the text boxes of one call together, that is one element: all its boxes are reduced by the same scale, so each keeps its weight | each box on its own - text is collected one line per box, so no line would ever reach the limit and a long text would not be bounded at all; the whole page - every page taller than two viewports would have all its text sampled, small labels included, to guard against a page nobody has seen |

- Ceiling, marked in the code: the bound on `text_backgrounds` is per element. A page of many texts, each under the limit, all over an image of millions of distinct colours, still pays for each of them. Over fills, gradients and photos that cost is small (see the measurement above).

## Checks

### S1 - `inspect_element` on a large element · 4 files · 27 KB · ~7k

**C1** - `inspect_element` on `#noise` (1440x10000, every pixel its own colour) succeeds and takes less than 3s longer than the same call on `#big-text`, a small element of the same page
Proof: `uv run pytest "tests/test_inspect_element.py::test_an_element_of_millions_of_colours_adds_little_to_the_call" -v`

**C2** - `#halves` (1024x1024, four times the limit: red above, blue below) reports `sampledColors == [{"hex": "#ff0000", "share": 0.5}, {"hex": "#0000ff", "share": 0.5}]`: the painted colours and no blend of them
Proof: `uv run pytest "tests/test_inspect_element.py::test_a_region_over_the_limit_keeps_its_painted_colours_and_shares" -v`

**C3** - The colours sampled from the existing fixtures are unchanged, with the tests unedited
Proof: `uv run pytest "tests/test_inspect_element.py::test_sampled_colors_are_the_painted_colors_by_share" -v`
Proof: `uv run pytest "tests/test_inspect_element.py::test_sampled_colors_keep_the_three_most_frequent" -v`
Proof: `uv run pytest "tests/test_inspect_element.py::test_sampled_color_is_the_painted_one_not_the_computed_one" -v`
Proof: `git diff b26d672..HEAD -- tests/test_inspect_element.py` shows added lines only

### S2 - `low-contrast-real` on a large text · 3 files · 24 KB · ~6k

**C4** - `detect_visual_bugs` with `low-contrast-real` on the page with `#over-noise` painted (three glyphs of 1440x1440 over the noise) succeeds and takes less than 10s longer than on the same page without it
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_text_over_millions_of_colours_adds_little_to_the_call" -v`

**C5** - `#big-text` (one glyph of 600x600, more than the limit, with a light band behind its last fifth) is reported with `contrastRatio == 1.6` and `sampledBackground == "#cccccc"`
Proof: `uv run pytest "tests/test_low_contrast_real.py::test_a_text_over_the_limit_is_still_judged_on_its_worst_part" -v`

**C6** - Every existing test of `low-contrast-real` passes unedited
Proof: `uv run pytest tests/test_low_contrast_real.py -v`
Proof: `git diff b26d672..HEAD -- tests/test_low_contrast_real.py` shows added lines only

### S3 - The limit and the record · 2 files · 6 KB · ~2k

**C7** - `config.py` defines `COLOR_COUNT_MAX_PIXELS` under a `# Source:` comment, and `vision.py` reads it from `config`
Proof: `grep -n -B6 "^COLOR_COUNT_MAX_PIXELS" src/squint_mcp/config.py` shows the `# Source:` comment
Proof: `grep -n "config.COLOR_COUNT_MAX_PIXELS" src/squint_mcp/vision.py` prints one line or more

**C8** - `CHANGELOG.md` has an entry under `[Unreleased]` saying that a region of more than 262,144 pixels is sampled before its colours are counted
Proof: `grep -n "262,144" CHANGELOG.md` prints a line under `## [Unreleased]`

**C9** - The files held for the release are not in the diff
Proof: `git diff --name-only b26d672..HEAD -- README.md pyproject.toml` prints nothing

### S4 - Gate

**C10** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: not in scope - no input surface changes
- failure modes: a region or a text box with no pixels on the page still yields nothing - existing `tests/test_inspect_element.py::test_element_with_no_rendered_box_is_an_error` and `tests/test_low_contrast_real.py::test_text_without_a_box_is_not_reported`; a reduced side never rounds down to 0 pixels (`max(1, ...)`)
- idempotency: the reduction has no randomness - existing `tests/test_low_contrast_real.py::test_the_same_call_returns_the_same_content`
- authorization: not in scope
- concurrency: the work stays synchronous on the event loop; bounded, it holds the loop for a fraction of a second per element instead of tens of seconds - C1, C4
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency; `Image.resize` is Pillow, already required
- state transitions: not in scope
- observability: not in scope - no log requirement; the result does not say that a region was sampled, and adding a field is a schema change nobody asked for

## Handoff

S1-S4 = ~15k of reading, one surface (`vision.py`). One agent, no handoff.

- What the user settled mid-build: C4 was written as "less than 3s longer". With the fix the call takes 2.3s longer, not the fraction of a second the count itself takes: for each distinct colour behind a text the Check computes a contrast, about 2s for 262,144 of them, and the measurement moves by about 1s between runs. Offered the choice between lowering the limit to 256x256 (measured +0.1s, but every element over 256x256 would be sampled) and keeping 512x512 with C4 at 10s, the user chose the second. Without the fix the same call takes 45s longer, so the test still fails without it.
- So the worst case of one text element, at the limit and over noise, is about 2s on the event loop, not half a second.
