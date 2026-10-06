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
