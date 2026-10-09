"""Crop, downscale and colour sampling over a Capture's pixels. No browser access."""

import io
import math
import random
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


def _bounds(pixels: Image.Image, box: Box, margin: int) -> tuple[int, int, int, int]:
    """The left, top, right and bottom of `box` grown by `margin`, clamped to the page.

    Boxes can be fractional (text spans are): round outwards so nothing is cut.
    A box entirely outside the page has no width or no height.
    """
    left = max(0, math.floor(box.x) - margin)
    top = max(0, math.floor(box.y) - margin)
    right = max(left, min(pixels.width, math.ceil(box.x + box.w) + margin))
    bottom = max(top, min(pixels.height, math.ceil(box.y + box.h) + margin))
    return left, top, right, bottom


def _region(pixels: Image.Image, box: Box, margin: int) -> Image.Image:
    """The pixels of `box` grown by `margin`, clamped to the page."""
    return pixels.crop(_bounds(pixels, box, margin))


def area(pixels: Image.Image, boxes: list[Box]) -> int:
    """How many pixels of the page `boxes` hold together."""
    total = 0
    for box in boxes:
        left, top, right, bottom = _bounds(pixels, box, 0)
        total += (right - left) * (bottom - top)
    return total


def count_limit(areas: list[int]) -> float:
    """The most pixels counted of any one of the things of `areas` pixels, so that
    no more than `COLOR_COUNT_MAX_PIXELS` are counted of all of them together.

    One of fewer pixels is counted whole and each larger one is sampled down to
    the limit, whatever the order they come in.
    """
    left = config.COLOR_COUNT_MAX_PIXELS
    for index, pixels in enumerate(sorted(areas)):
        larger = len(areas) - index
        if pixels * larger > left:
            return left / larger
        left -= pixels
    return math.inf


def _rows(image: Image.Image, count: int) -> Image.Image:
    """`count` rows of `image`, one from each of as many bands of equal height."""
    # A fixed seed: the same rows on every call. At an offset of its own in each
    # band, because rows picked at a regular step all land on one colour of a
    # pattern whose period divides the step.
    offsets = random.Random(0)
    stride = image.width * len(image.getbands())
    data = image.tobytes()
    picked = (
        int((index + offsets.random()) * image.height / count) for index in range(count)
    )
    return Image.frombytes(
        image.mode,
        (image.width, count),
        b"".join(data[row * stride : (row + 1) * stride] for row in picked),
    )


def _countable(region: Image.Image, area: int, limit: float) -> Image.Image:
    """`region` at the scale that brings `area` pixels down to `limit`.

    `area` is that of everything counted together, of which `region` is a part.
    Counting colours costs the most where every pixel has its own (issue #4).
    """
    if area <= limit:
        return region
    scale = math.sqrt(limit / area)
    # ponytail: a part keeps at least one pixel, so more parts than the limit
    # has pixels are counted past it.
    width = max(1, int(region.width * scale))
    height = max(1, int(region.height * scale))
    # Pixels are picked, never blended: a filter would make colours, and amounts
    # of ink, that the page never painted.
    rows = _rows(region, height)
    return _rows(rows.transpose(Image.Transpose.TRANSPOSE), width).transpose(
        Image.Transpose.TRANSPOSE
    )


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
    background: Image.Image, ink: Image.Image, boxes: list[Box], limit: float
) -> list[tuple[int, tuple[int, int, int]]]:
    """The colours painted behind the text inside `boxes`, each with how many text
    pixels it lies behind.

    `background` is the page without its text and `ink` how much text ink each
    pixel gets (AD-004). Empty when no pixel of the boxes is text. Boxes of more
    pixels together than `limit` are sampled, so the counts are of the sample.
    """
    is_text = [255 if value >= config.TEXT_INK_MIN else 0 for value in range(256)]
    counts: Counter[tuple[int, int, int]] = Counter()
    regions = [_region(background, box, 0) for box in boxes]
    # One scale for all the boxes, so that each keeps about its weight in the counts.
    together = sum(region.width * region.height for region in regions)
    for box, region in zip(boxes, regions, strict=True):
        if region.width * region.height == 0:
            continue
        behind = _countable(region, together, limit)
        # With the text pixels as its opaque ones, the region counts its colours
        # apart for text and for the rest.
        # Pillow types `point` for every kind of table it takes, some of them untyped.
        text = _countable(_region(ink, box, 0), together, limit).point(is_text)  # pyright: ignore[reportUnknownMemberType]
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
    region = _countable(
        region, region.width * region.height, config.COLOR_COUNT_MAX_PIXELS
    )
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
