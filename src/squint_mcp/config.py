"""Thresholds and defaults, each with its source cited."""

# Source: docs/SPEC.md, Further Notes: a single desktop size, as in the draft's example.
DEFAULT_VIEWPORT_WIDTH = 1440
DEFAULT_VIEWPORT_HEIGHT = 900

# Source: docs/SPEC.md, Tools: "a total timeout of 30s with a clear error".
TOTAL_TIMEOUT_S = 30.0

# Source: docs/SPEC.md, Stabilization: "networkidle with a timeout of about 3s".
NETWORK_IDLE_TIMEOUT_S = 3.0

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
# properties plus `direction`, which tells a Check on which edge text is cut, and
# `-webkit-text-fill-color`, the colour that paints the glyphs: that of `color`
# unless the page sets it.
CAPTURE_COMPUTED_PROPERTIES = (
    *INSPECT_COMPUTED_PROPERTIES,
    "direction",
    "-webkit-text-fill-color",
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
