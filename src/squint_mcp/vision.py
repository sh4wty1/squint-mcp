"""Crop, downscale and colour sampling over a Capture's pixels. No browser access."""

import io
import math
from collections import Counter
from typing import cast

from PIL import Image
from pydantic import BaseModel

from squint_mcp import config
from squint_mcp.models import Box


class SampledColor(BaseModel):
    hex: str
    share: float
    """Fraction of the element's pixels painted in this colour."""


def _region(pixels: Image.Image, box: Box, margin: int) -> Image.Image:
    """The pixels of `box` grown by `margin`, clamped to the page.

    Boxes can be fractional (text spans are): round outwards so nothing is cut.
    A box entirely outside the page yields an empty region.
    """
    left = max(0, math.floor(box.x) - margin)
    top = max(0, math.floor(box.y) - margin)
    right = max(left, min(pixels.width, math.ceil(box.x + box.w) + margin))
    bottom = max(top, min(pixels.height, math.ceil(box.y + box.h) + margin))
    return pixels.crop((left, top, right, bottom))


def crop_png(pixels: Image.Image, box: Box) -> bytes:
    """A PNG of the element with a margin around it, small enough to be cheap."""
    region = _region(pixels, box, config.CROP_MARGIN_PX)
    # thumbnail() keeps the aspect ratio and never upscales.
    region.thumbnail((config.CROP_MAX_SIDE_PX, config.CROP_MAX_SIDE_PX))
    buffer = io.BytesIO()
    region.save(buffer, format="PNG")
    return buffer.getvalue()


def is_flat(pixels: Image.Image, box: Box) -> bool:
    """Whether `box` is painted in a single colour. A box with no pixels is flat."""
    region = _region(pixels, box, 0)
    # getcolors() gives up, returning None, past `maxcolors` distinct colours.
    return (
        region.width * region.height == 0 or region.getcolors(maxcolors=1) is not None
    )


def text_backgrounds(
    background: Image.Image, ink: Image.Image, boxes: list[Box]
) -> list[tuple[int, tuple[int, int, int]]]:
    """The colours painted behind the text inside `boxes`, each with how many text
    pixels it lies behind.

    `background` is the page without its text and `ink` how much text ink each
    pixel gets (AD-004). Empty when no pixel of the boxes is text.
    """
    is_text = [255 if value >= config.TEXT_INK_MIN else 0 for value in range(256)]
    counts: Counter[tuple[int, int, int]] = Counter()
    for box in boxes:
        behind = _region(background, box, 0)
        area = behind.width * behind.height
        if area == 0:
            continue
        # With the text pixels as its opaque ones, the region counts its colours
        # apart for text and for the rest.
        # Pillow types `point` for every kind of table it takes, some of them untyped.
        text = _region(ink, box, 0).point(is_text)  # pyright: ignore[reportUnknownMemberType]
        behind.putalpha(text)
        colors = cast(
            "list[tuple[int, tuple[int, int, int, int]]]",
            behind.getcolors(maxcolors=area),
        )
        for count, (red, green, blue, alpha) in colors:
            if alpha:
                counts[red, green, blue] += count
    return [(count, color) for color, count in counts.items()]


def sample_colors(pixels: Image.Image, box: Box) -> list[SampledColor]:
    """The most frequent colours painted inside the element's border box.

    Empty when the box has no pixels on the page.
    """
    region = _region(pixels, box, 0)
    total = region.width * region.height
    if total == 0:
        return []
    # ponytail: exact colour counts, so a gradient or a photo reports thin bands.
    # Cluster the colours when a Check needs perceptual ones.
    counts = cast(
        "list[tuple[int, tuple[int, int, int]]]", region.getcolors(maxcolors=total)
    )
    top = sorted(counts, reverse=True)[: config.SAMPLED_COLORS_MAX]
    return [
        SampledColor(
            hex="#{:02x}{:02x}{:02x}".format(*rgb), share=round(count / total, 4)
        )
        for count, rgb in top
    ]
