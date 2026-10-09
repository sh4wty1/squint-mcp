# Pixel budget per Capture

Roadmap slice 6. Issue #11.

## Problem

`low-contrast-real` bounds its colour counting per element: each text is sampled down to 262,144 pixels on its own. A page of many texts, each under that limit, all over an image of millions of distinct colours, pays for every one of them, after the 30s clock of the call has stopped. Measured on `f2c6213`: 55 texts of 1440x180 (259,200 pixels each) over noise take the Check **61.8s**. Issue #11 measured 4.5s for 27 of them and 8.25s for 54 of 512x512. Whoever calls `detect_visual_bugs` on such a page waits a minute past the timeout the tool documents.

When a region is sampled, the pixels are picked on a regular grid. At a scale of one half that is every other row, so a pattern with a 2px period loses one of its colours. Issue #11: 1px rows alternating red and blue, 1024x1024, are reported by `inspect_element` as `#0000ff` at share 1.0; the same stripes behind a text are judged against blue only. The caller gets a colour share, or a contrast, that the page does not have.

When this ships: the pixel work of `low-contrast-real` on one Capture is bounded whatever the number of texts, and a sampled region reports every colour of a fine pattern in about its painted share.

## Flow

Reuses `_region`, `_countable`, `text_backgrounds` and the one limit `COLOR_COUNT_MAX_PIXELS`: no new module, and nothing changes in the Capture, the Finding or the tools.

1. a Capture -> `detect_visual_bugs` (exists) - unchanged, hands it to each Check
2. `checks/low_contrast_real.py` (exists) - before judging, adds up the text area of the elements it judges and derives one cap per text for the Capture (door 1, door 2)
3. `vision.text_backgrounds` (exists) - samples the boxes of an element down to that cap instead of down to the fixed limit
4. `vision._countable` (exists) - picks the pixels of a sampled region at jittered offsets instead of on a regular grid (door 3); `vision.sample_colors` (exists) goes through it too, with its own region as the whole budget
5. out: the same `Finding` and the same `sampledColors`, read by `detect_visual_bugs` (exists) and `inspect_element` (exists)

## Impact

| Front | What changes |
| --- | --- |
| domain | no new term. `COLOR_COUNT_MAX_PIXELS` meant "per element" for text and now means "per Capture, across its texts"; for `inspect_element` it still means the one region. Only `vision.py` branches on it |
| results | on a page whose judged texts cover more than 262,144 pixels together, texts that were counted whole are now sampled. Measured on a 40,000px page of 343 texts and on the Wikipedia WCAG article (1,181 texts, 3.3M text pixels): the same Findings, ratios moving by at most 0.17 |
| results | every sampled region changes its exact numbers, because the pixels picked are others. Regions of 262,144 pixels or fewer, alone or together, are counted whole as before: every existing fixture but `pixel-cost.html` is under it (the largest, `selectors.html`, has 174,800) |
| existing test | `test_a_region_over_the_limit_keeps_its_painted_colours_and_shares` asserts `0.502` / `0.498`, "the shares of every other row": the regular grid itself. Its expected value changes to what AC 9 says. It is the only existing assertion edited |
| stored data | nothing to migrate - nothing is persisted |

## Relations

`None - no stored-data shape change`

## Surface

`None - no tool, parameter or field is added or changed; nothing new is consumed outside`

## Landing

Nothing here is persisted or a contract. The three rows are the choices that change the numbers a released tool reports, each settled by a spike on `f2c6213` (throwaway, not in the repo).

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1. How the budget is split | every text gets the same cap `c`, the largest with `sum(min(area, c)) <= budget`; a text of at most `c` pixels is counted whole, a larger one at scale `sqrt(c / area)`. Depends on no order | one scale `sqrt(budget / total area)` for the whole Capture - on the Wikipedia article it lost 3 of 22 Findings and left 50 texts with no text pixel in their sample, against 0 lost and 2 for the cap. Spending the budget in document order - the last texts of a page get nothing, and a Finding depends on what stands before it |
| 2. The budget | `COLOR_COUNT_MAX_PIXELS = 512 * 512`, the existing limit, now across the texts of a Capture. The 55 texts over noise: 61.8s -> 1.0s | `1024 * 1024` - no text left without a text pixel, but one text over noise would count four times what it does today (2.3s measured for issue #4), past the `< 10` the existing proof asserts. `2 * 512 * 512` - live alternative: 1 text without a text pixel instead of 2 (15 with door 3), at twice the worst case |
| 3. How a sampled region picks its pixels | output row `j` of `n` takes source row `int((j + u[j]) * height / n)`, `u` a fixed table from `random.Random(0)`; columns the same way; the same offsets for `background` and `ink`. Measured at one half: 1px rows 0.484 / 0.516, 1px checkerboard 0.4995 / 0.5005, `#halves` 0.5 / 0.5 | keeping the regular grid and documenting the limit - live alternative, and the cheaper one. Rejected because door 1 makes sampling ordinary (973 of 1,181 texts on the Wikipedia article, at steps of 2 to 12px), so the grid now meets the dotted and ruled backgrounds real pages have. An offset per pixel - a Python loop over every pixel, or a new dependency (numpy) |

- Cost of door 3, measured: 0.14s -> 0.27s for the Check on the Wikipedia article, and 15 texts instead of 2 left with no text pixel in their sample (none of them a Finding)
- Nothing else in this change is hard to reverse

## Criteria

### S1: the texts of a Capture share one budget (P1)

The pixel work of `low-contrast-real` on a Capture no longer grows with the number of texts.

**Acceptance Criteria**

1. WHEN `detect_visual_bugs` runs `low-contrast-real` on a page of 55 texts of 1440x180 over 1440x10000 of noise THEN the call SHALL succeed and take less than 10s longer than on the same page without those texts
2. WHILE the texts judged in a Capture cover 262,144 pixels or fewer together, the system SHALL count every one of them whole
3. WHEN the texts judged in a Capture cover more than 262,144 pixels together THEN the system SHALL count each text of at most `c` pixels whole and sample each larger one down to `c`, where `c` is the largest cap for which the pixels counted do not exceed 262,144
4. WHEN a text of 100x40 at 2.84:1 on a flat background stands on that page of 55 texts THEN the system SHALL report it with the `contrastRatio` and the `sampledBackground` it has on a page of its own
5. WHEN a text of 600x600 with a light band behind its last fifth stands on a page with another text of more than 262,144 pixels THEN the system SHALL still report it with `contrastRatio == 1.6` and `sampledBackground == "#cccccc"`
6. WHEN `detect_visual_bugs` is called twice on that page of 55 texts THEN the system SHALL return the same structured content both times
7. The system SHALL keep every existing test of `low-contrast-real` passing unedited

**Independent test:** call `detect_visual_bugs` on the new fixture with and without its texts targeted, and compare the seconds.

### S2: a sampled region keeps the colours of a fine pattern (P2)

`inspect_element` and `low-contrast-real` report a 1px or 2px pattern in about its painted shares.

**Acceptance Criteria**

8. WHEN `inspect_element` reads an element of 1024x1024 painted in 1px rows, in 1px columns or in a 1px checkerboard of red and blue THEN `sampledColors` SHALL hold exactly `#ff0000` and `#0000ff`, each with a share from 0.4 to 0.6
9. WHEN `inspect_element` reads `#halves` (1024x1024, red above row 511, blue from it down) THEN `sampledColors` SHALL hold exactly `#ff0000` and `#0000ff`, each with a share within 0.01 of the painted one (0.499 and 0.501)
10. WHEN `low-contrast-real` judges a white text of 600x600 over 1px rows alternating black and `#cccccc` THEN the system SHALL report it with `contrastRatio == 1.6` and `sampledBackground == "#cccccc"`, whichever of the two colours the first row has
11. WHEN `inspect_element` is called twice on one of those patterned elements THEN the system SHALL return the same `sampledColors` both times
12. WHILE a region has 262,144 pixels or fewer, `inspect_element` SHALL report the shares of all its pixels, as the existing tests assert

**Independent test:** `inspect_element` on the three patterned elements of the fixture.

### S3: the record (P3)

**Acceptance Criteria**

13. The `[Unreleased]` section of `CHANGELOG.md` SHALL say that `low-contrast-real` counts at most 262,144 pixels across the texts of a page, and that a sampled region no longer loses a colour of a 1px or 2px pattern
14. The `# Source:` comment of `COLOR_COUNT_MAX_PIXELS` in `config.py` SHALL say that for text the limit is per Capture
15. The `ponytail:` comment of `text_backgrounds` that points at #11 SHALL be gone

**Independent test:** read the three places.

## Out of scope

| Excluded | Why |
| --- | --- |
| Making the pixel work cancellable, or moving it off the event loop | roadmap slice 6, "Não entra" |
| A pool of browsers | roadmap slice 6, "Não entra" |
| A field saying that a result was sampled | a change to the Finding and to `sampledColors`; roadmap slice 6, "Não entra" |
| One budget for all the viewports of a call | the roadmap says per Capture; a call of n viewports has n budgets |
| A budget on distinct colours instead of pixels | what the cost really follows, but the roadmap and issue #11 ask for counted pixels |
| Guaranteeing a text pixel in the sample of every text | needs a floor per text, which is no longer a bound; see Assumptions |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| The budget value | 262,144, the existing constant | door 2: the worst case of a Capture becomes what issue #4 accepted for one element, and the existing timing proofs hold unedited | n |
| The aliasing decision | fix it, with the jitter of door 3 | door 3: the budget makes sampling ordinary. Costs 0.13s on a 1,181-text page and exact shares on sampled regions | n |
| Which texts share the budget | those the Check reads pixels for: own text, opacity 1, an sRGB fill that is not transparent; their boxes clamped to the page | a text the Check skips costs nothing, so it should take no share | n |
| A text whose sample holds no text pixel | not judged, as a text with no ink is today | measured: 15 of 1,181 texts on the Wikipedia article, 5 of 343 on the long page, none of them a Finding - texts of almost no ink, such as a separator | n |
| `inspect_element` | keeps `COLOR_COUNT_MAX_PIXELS` for its one region | one element per call: the region is already the whole budget | n |
| The bound of AC 1 | 10s, as the proofs of issue #4 | measured 1.0s; the same margin for a slow CI runner | n |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| tools `detect_visual_bugs`, `inspect_element` | response shape | existing - no field added, removed or renamed |
| tools `detect_visual_bugs`, `inspect_element` | error shape and codes | n/a - no new failure: a sample is never of zero pixels (`max(1, ...)`, existing) |
| tools `detect_visual_bugs`, `inspect_element` | who may call, rate limits | n/a - a local stdio server, as before |
| tools `detect_visual_bugs`, `inspect_element` | versioning | AC 13 - a changed threshold is recorded in the CHANGELOG, not a breaking change |
| document `CHANGELOG.md` | structure, depth | AC 13 - one entry under `[Unreleased]`, in the form of the existing ones |

## Sources

- https://github.com/sh4wty1/squint-mcp/issues/11 - the two defects, the measurements, the direction for the first and the determinism the second must keep
- `docs/ROADMAP.md`, section 6 - what enters and what does not
- `.checks/issue4-pixel-work-bound.md` - the per-element bound this replaces, and the timing proofs that must keep passing
