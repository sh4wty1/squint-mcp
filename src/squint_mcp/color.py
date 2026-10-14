"""Colours as numbers. No browser code and no Capture here."""

import math

Lab = tuple[float, float, float]
"""A CIE Lab colour: L, a and b."""

Srgb = tuple[float, float, float, float]
"""An sRGB colour: red, green and blue on the scale 0 to 1, and the alpha."""


def parse(text: str) -> Srgb | None:
    """The colour of a computed `rgb(r, g, b)` or `rgba(r, g, b, a)`, or of a
    `color(srgb r g b)` or `color(srgb r g b / a)`, where a component of `none`
    is 0; None for any other text."""
    if not text.endswith(")"):
        return None
    if text.startswith(("rgb(", "rgba(")):
        channels = text[text.index("(") + 1 : -1].split(",")
        red, green, blue, *alpha = (float(channel) for channel in channels)
        return red / 255, green / 255, blue / 255, alpha[0] if alpha else 1.0
    if text.startswith("color(srgb "):
        parts = text.removeprefix("color(srgb ")[:-1].replace("/", " ").split()
        red, green, blue, *alpha = (
            0.0 if part == "none" else float(part) for part in parts
        )
        return red, green, blue, alpha[0] if alpha else 1.0
    return None


def to_hex(color: Srgb) -> str:
    """`#rrggbb` in lower case, each channel rounded half up to 8 bits and clipped
    to them; `#rrggbbaa` when the alpha, rounded the same way, is below 255."""
    red, green, blue, alpha = (
        min(max(math.floor(channel * 255 + 0.5), 0), 255) for channel in color
    )
    opaque = f"#{red:02x}{green:02x}{blue:02x}"
    return opaque if alpha == 255 else f"{opaque}{alpha:02x}"


def delta_e_2000(reference: Lab, sample: Lab) -> float:
    """The CIEDE2000 colour difference of two Lab colours.

    The formula of CSS Color Module Level 4, section 20.2, as Sharma, Wu and
    Dalal (2005) write it, with kL, kC and kH at 1.
    """
    l1, a1, b1 = reference
    l2, a2, b2 = sample
    c_mean = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(c_mean**7 / (c_mean**7 + 25**7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    # A colour with no chroma has no hue: its angle is 0.
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0

    dl = l2 - l1
    dc = c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    elif abs(h2p - h1p) <= 180:
        dh = h2p - h1p
    elif h2p - h1p > 180:
        dh = h2p - h1p - 360
    else:
        dh = h2p - h1p + 360
    dhp = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))

    l_mean = (l1 + l2) / 2
    cp_mean = (c1p + c2p) / 2
    if c1p * c2p == 0:
        h_mean = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        h_mean = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        h_mean = (h1p + h2p + 360) / 2
    else:
        h_mean = (h1p + h2p - 360) / 2
    t = (
        1
        - 0.17 * math.cos(math.radians(h_mean - 30))
        + 0.24 * math.cos(math.radians(2 * h_mean))
        + 0.32 * math.cos(math.radians(3 * h_mean + 6))
        - 0.20 * math.cos(math.radians(4 * h_mean - 63))
    )
    d_theta = 30 * math.exp(-(((h_mean - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cp_mean**7 / (cp_mean**7 + 25**7))
    sl = 1 + 0.015 * (l_mean - 50) ** 2 / math.sqrt(20 + (l_mean - 50) ** 2)
    sc = 1 + 0.045 * cp_mean
    sh = 1 + 0.015 * cp_mean * t
    rt = -math.sin(math.radians(2 * d_theta)) * rc
    return math.sqrt(
        (dl / sl) ** 2 + (dc / sc) ** 2 + (dhp / sh) ** 2 + rt * (dc / sc) * (dhp / sh)
    )
