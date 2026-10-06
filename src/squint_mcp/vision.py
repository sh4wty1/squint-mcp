"""Crop, downscale and colour sampling over a Capture's pixels. No browser access."""

import io
import math
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
    """
    return pixels.crop(
        (
            max(0, math.floor(box.x) - margin),
            max(0, math.floor(box.y) - margin),
            min(pixels.width, math.ceil(box.x + box.w) + margin),
            min(pixels.height, math.ceil(box.y + box.h) + margin),
        )
    )


def crop_png(pixels: Image.Image, box: Box) -> bytes:
    """A PNG of the element with a margin around it, small enough to be cheap."""
    region = _region(pixels, box, config.CROP_MARGIN_PX)
    # thumbnail() keeps the aspect ratio and never upscales.
    region.thumbnail((config.CROP_MAX_SIDE_PX, config.CROP_MAX_SIDE_PX))
    buffer = io.BytesIO()
    region.save(buffer, format="PNG")
    return buffer.getvalue()


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
