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


def _countable(region: Image.Image, area: int) -> Image.Image:
    """`region` at the scale that brings `area` pixels down to as many as are counted.

    `area` is that of everything counted together, of which `region` is a part.
    Counting colours costs the most where every pixel has its own (issue #4).
    """
    if area <= config.COLOR_COUNT_MAX_PIXELS:
        return region
    scale = math.sqrt(config.COLOR_COUNT_MAX_PIXELS / area)
    size = (max(1, int(region.width * scale)), max(1, int(region.height * scale)))
    # NEAREST picks pixels: any other filter blends neighbours into colours, and
    # into amounts of ink, that the page never painted.
    # Pillow types `resize` for every kind of size it takes, some of them untyped.
    return region.resize(size, Image.Resampling.NEAREST)  # pyright: ignore[reportUnknownMemberType]


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
    pixel gets (AD-004). Empty when no pixel of the boxes is text. Boxes of more
    pixels together than are counted are sampled, so the counts are of the sample.
    """
    is_text = [255 if value >= config.TEXT_INK_MIN else 0 for value in range(256)]
    counts: Counter[tuple[int, int, int]] = Counter()
    regions = [_region(background, box, 0) for box in boxes]
    # One scale for all the boxes, so that each keeps its weight in the counts.
    # ponytail: bounded per call, that is per element. A page of many texts over
    # an image of millions of colours pays for each; share one budget across the
    # Capture if such a page gets slow.
    area = sum(region.width * region.height for region in regions)
    for box, region in zip(boxes, regions, strict=True):
        if region.width * region.height == 0:
            continue
        behind = _countable(region, area)
        # With the text pixels as its opaque ones, the region counts its colours
        # apart for text and for the rest.
        # Pillow types `point` for every kind of table it takes, some of them untyped.
        text = _countable(_region(ink, box, 0), area).point(is_text)  # pyright: ignore[reportUnknownMemberType]
        behind.putalpha(text)
        colors = cast(
            "list[tuple[int, tuple[int, int, int, int]]]",
            behind.getcolors(maxcolors=behind.width * behind.height),
        )
        for count, (red, green, blue, alpha) in colors:
            if alpha:
                counts[red, green, blue] += count
    return [(count, color) for color, count in counts.items()]


def sample_colors(pixels: Image.Image, box: Box) -> list[SampledColor]:
    """The most frequent colours painted inside the element's border box.

    Empty when the box has no pixels on the page. A box of more pixels than are
    counted is sampled, so its shares are those of the sample.
    """
    region = _region(pixels, box, 0)
    if region.width * region.height == 0:
        return []
    region = _countable(region, region.width * region.height)
    total = region.width * region.height
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
