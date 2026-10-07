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
# properties plus `direction`, which tells a Check on which edge text is cut.
CAPTURE_COMPUTED_PROPERTIES = (*INSPECT_COMPUTED_PROPERTIES, "direction")

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
