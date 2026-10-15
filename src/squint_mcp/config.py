"""Thresholds and defaults, each with its source cited."""

# Source: docs/SPEC.md, Further Notes: a single desktop size, as in the draft's example.
DEFAULT_VIEWPORT_WIDTH = 1440
DEFAULT_VIEWPORT_HEIGHT = 900

# Source: docs/SPEC.md, Tools: "a total timeout of 30s with a clear error".
TOTAL_TIMEOUT_S = 30.0

# Source: docs/SPEC.md, Stabilization: "networkidle with a timeout of about 3s".
NETWORK_IDLE_TIMEOUT_S = 3.0

# Source: Squint default (AD-006). Text is anti-aliased in grayscale: with subpixel
# text Chromium rasterizes the same glyph differently over different backdrops, and
# ink measured in two renders of a page cannot be compared.
CHROMIUM_ARGS = ("--disable-lcd-text",)

# Source: Squint default (AD-007), measured for slice 8. The two frames a Capture
# lets a page paint before a screenshot take about 30ms, and up to 90ms were
# measured. A page that never calls an animation frame back is waited on this
# long before each screenshot and is then captured as it is.
PAINT_WAIT_MAX_S = 0.25

# Source: Squint default. docs/SPEC.md asks for "a margin around the element";
# 16px shows the surroundings without doubling the size of a small crop.
CROP_MARGIN_PX = 16

# Source: docs/SPEC.md, Images: "downscaled to about 512px on its longest side".
CROP_MAX_SIDE_PX = 512

# Source: Squint default. On text over a flat fill, the three most frequent colours
# are the fill, the text and the dominant anti-aliasing blend.
SAMPLED_COLORS_MAX = 3

# Source: Squint default, measured for issue #4. Counting the colours of a region
# where every pixel has its own takes about 2 microseconds a pixel: 15s for an
# element of 1440x5000. At 512x512 it stays under half a second, and the contrast
# of as many colours behind a text takes about two. A larger region is sampled
# down to that many pixels first. For text the limit is per Capture: the texts a
# Check judges share it (issue #11).
COLOR_COUNT_MAX_PIXELS = 512 * 512

# Source: Squint default. Chromium resolves 350+ properties; these are the ones that
# decide how a box and its text are painted. Margin, border and padding are reported
# in the box model instead.
INSPECT_COMPUTED_PROPERTIES = (
    "display",
    "position",
    "box-sizing",
    "width",
    "height",
    "color",
    "background-color",
    "background-image",
    "opacity",
    "visibility",
    "overflow-x",
    "overflow-y",
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "letter-spacing",
    "text-align",
    "text-overflow",
    "white-space",
)

# Source: Squint default. What a Capture collects for every element: the inspect
# properties plus `direction`, which tells a Check on which edge text is cut,
# `-webkit-text-fill-color`, the colour that paints the glyphs: that of `color`
# unless the page sets it, `z-index`, which with `position` decides what is
# painted above an element, and `font-style`, which with `font-family` and
# `font-weight` says which face of a family an element asks for. The twelve
# after them are what the tokens of a page are made of besides the box model
# (AD-009): the colour of each border, the radius of each corner, the two
# shadows and the two gaps.
CAPTURE_COMPUTED_PROPERTIES = (
    *INSPECT_COMPUTED_PROPERTIES,
    "direction",
    "-webkit-text-fill-color",
    "z-index",
    "font-style",
    "border-top-color",
    "border-right-color",
    "border-bottom-color",
    "border-left-color",
    "border-top-left-radius",
    "border-top-right-radius",
    "border-bottom-right-radius",
    "border-bottom-left-radius",
    "box-shadow",
    "text-shadow",
    "row-gap",
    "column-gap",
)

# Source: Squint default (AD-009). Those of the list above whose computed value
# is one colour, which Chromium writes in the notation the page wrote it in.
CAPTURE_COLOR_PROPERTIES = (
    "color",
    "background-color",
    "-webkit-text-fill-color",
    "border-top-color",
    "border-right-color",
    "border-bottom-color",
    "border-left-color",
)

# Source: Squint default (AD-008). What changes the width of a text or the
# characters painted, besides the `font-` properties, which the page script
# takes from the computed style: a copy of a text carries them.
TEXT_SHAPING_PROPERTIES = (
    "letter-spacing",
    "word-spacing",
    "text-transform",
    "text-rendering",
    "direction",
)

# Source: docs/SPEC.md, Images: "At most five crops per call".
MAX_CROPS = 5

# Source: docs/SPEC.md, Finding: "visible text excerpt, ~40 chars".
TEXT_EXCERPT_MAX_CHARS = 40

# Source: Squint default. scrollWidth and clientWidth are rounded integers, so a
# difference of 1px can be rounding alone.
TEXT_CLIPPED_MIN_OVERFLOW_PX = 2

# Source: Squint default. A cut of 8px or more takes a glyph or most of one at body
# sizes and is `major`; a smaller one is `minor`.
TEXT_CLIPPED_MAJOR_OVERFLOW_PX = 8

# Source: docs/adr/0003. An element whose painted size differs from its layout size
# by this much is under a transform. The collector is passed the same value.
TRANSFORM_MIN_SIZE_DIFF_PX = 1

# Source: Squint default. A page scrolls by whole pixels and a box can end on a
# fraction of one, so the element that sets the width of a page ends less than
# 1px from the page's right edge.
OFFSCREEN_OVERFLOW_EDGE_TOLERANCE_PX = 1

# Source: WCAG 2.2 SC 1.4.3 Contrast (Minimum): "a contrast ratio of at least 4.5:1".
CONTRAST_MIN_RATIO = 4.5

# Source: WCAG 2.2 SC 1.4.3: "Large-scale text [has] a contrast ratio of at least 3:1".
CONTRAST_MIN_RATIO_LARGE = 3.0

# Source: WCAG 2.2, "large scale": at least 18 point, which is 24 CSS pixels.
LARGE_TEXT_MIN_PX = 24.0

# Source: WCAG 2.2, "large scale": at least 14 point bold, "typically 18.66px".
LARGE_BOLD_TEXT_MIN_PX = 18.66

# Source: CSS Fonts: the `bold` keyword computes to a font-weight of 700.
BOLD_MIN_WEIGHT = 700

# Source: Squint default. 3:1 is the lowest ratio WCAG accepts for any text: under
# it the Finding is `major`, from it up to the required ratio it is `minor`.
LOW_CONTRAST_MAJOR_BELOW_RATIO = 3.0

# Source: Squint default. Over a background that varies, the worst tenth of the
# text decides: one glyph in a word of ten. A title that half disappears is caught
# and a few stray pixels of a photo are not.
LOW_CONTRAST_WORST_PART_PERCENT = 10

# Source: Squint default. Ink runs from 0 to 255: a pixel at least half covered by
# a glyph is text, a fainter anti-aliased edge is background.
TEXT_INK_MIN = 128

# Source: Squint default. A text is reported as covered from a tenth of its ink
# hidden: one glyph in a word of ten, the share `low-contrast-real` takes as its
# worst part. The smallest real bug measured for slice 8 hid 13%, a badge none.
OVERLAP_MIN_HIDDEN_PERCENT = 10

# Source: Squint default. A quarter of a text gone leaves a sentence or a price
# unreadable and is `major`; less than that costs a word and is `minor`.
OVERLAP_MAJOR_HIDDEN_PERCENT = 25

# Source: WAI-ARIA 1.2, the roles of the widgets that open over a page: `menu`,
# `listbox`, `tooltip`, `dialog` and `alertdialog`. What an element of one of
# them covers is meant to be covered (decided with the maintainer for slice 8).
SILENT_LAYER_ROLES = ("menu", "listbox", "tooltip", "dialog", "alertdialog")

# Source: Squint default, measured for slice 8. A hit test takes 30 to 60
# microseconds: at most this many per Capture keep them to about a second. A
# Capture with more hidden pixels than that tests a sample of them.
HIT_TEST_MAX = 20_000

# Source: CSS Color Module Level 4, section 20.2 for the formula, ΔE2000, and the
# note of section 14.2.1 for the value: "using deltaE2000, one JND is 2". The
# module compares with `E < JND`, so two colours are Near below 2. It gives that
# just noticeable difference for gamut mapping: reading it as "two colours a
# viewer cannot tell apart are one token" is Squint's.
TOKENS_NEAR_COLOR_BELOW_DELTA_E = 2.0

# Source: Squint default, no norm found. A Capture has one image pixel per CSS
# pixel, so two px lengths less than 1px apart are Near, and the whole steps of
# a scale (12, 13, 14) stay apart.
TOKENS_NEAR_LENGTH_BELOW_PX = 1.0

# Source: Squint default, not measured on real pages. Eight Families of 20 bound
# a response to 160 Tokens, and a scale longer than 20 says so through `total`.
TOKENS_MAX_PER_FAMILY = 20
