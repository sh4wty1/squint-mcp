"""Covered text: how much of the ink of a text is hidden, read from the layers a
Capture takes for it (AD-005). Arithmetic on boxes and pixels; no browser access.
"""

import itertools
import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from PIL import Image, ImageChops

from squint_mcp import config, vision
from squint_mcp.models import Box, Element

# The left, top, right and bottom of a rectangle, in whole pixels of the page.
type Bounds = tuple[int, int, int, int]

# How much ink each pixel gets, 0 to 255, from the glyphs marked on each of the
# three channels of a pair of screenshots.
type Layers = tuple[Image.Image, Image.Image, Image.Image]

_IS_TEXT = [255 if value >= config.TEXT_INK_MIN else 0 for value in range(256)]
_DOUBLE = [min(255, 2 * value) for value in range(256)]
_NONZERO = [255 if value else 0 for value in range(256)]

# The green highlight is painted at a quarter of the strength of the red and the
# blue ones, which Chromium rasterizes as it does black (js/covered_text.js).
_GREEN = [min(255, 4 * value) for value in range(256)]

# Phase 1 takes a pixel that gets this much ink of another text for one where that
# text may be hiding this one. Under what makes a pixel text: the edge of a glyph
# is not rasterized alike in a colour and in black, and the bound has to err
# towards measuring.
_OTHER_INK_MIN = 64
_IS_OTHER = [255 if value >= _OTHER_INK_MIN else 0 for value in range(256)]

# Texts are looked up by the cells of a grid their boxes touch. A line of body
# text is some 20px high: a cell holds a few of them.
_CELL_PX = 64


@dataclass
class Text:
    """An element with own text, as the cover script describes it."""

    index: int
    """Its place among the elements of the Capture."""
    ancestors: frozenset[int]
    region: Bounds
    """What it paints together with what is inside it."""
    layers: tuple[int, ...]
    """The roots of its Silent layers."""
    boxes: list[Bounds]
    """The boxes of its own text that hold pixels of the page."""
    bounds: Bounds
    """The smallest rectangle that holds `boxes`."""
    round: int = 0
    channel: int = 0
    """Which pair of screenshots of phase 1, and which channel of it, tells its
    glyphs from those of the texts around it."""


def _through(image: Image.Image, table: list[int]) -> Image.Image:
    # Pillow types `point` for every kind of table it takes, some of them untyped.
    return image.point(table)  # pyright: ignore[reportUnknownMemberType]


def _count(mask: Image.Image) -> int:
    """How many pixels of `mask`, which holds only 0 and 255, are set."""
    return mask.histogram()[255]


def _crosses(one: Bounds, other: Bounds) -> bool:
    return (
        one[0] < other[2]
        and other[0] < one[2]
        and one[1] < other[3]
        and other[1] < one[3]
    )


def _own_text(text: Text) -> Image.Image:
    """The pixels of the bounds of `text` that are inside a box of its own text."""
    left, top, right, bottom = text.bounds
    mask = Image.new("L", (right - left, bottom - top), 0)
    for box in text.boxes:
        mask.paste(255, (box[0] - left, box[1] - top, box[2] - left, box[3] - top))
    return mask


def _unseen(alone: Image.Image, shown: Image.Image) -> Image.Image:
    """The pixels where less than half of the ink a text has alone shows.

    In integers: seen is twice the ink that shows being at least the ink alone,
    so the same veil gives one answer on a full glyph and on a faint edge.
    """
    return _through(ImageChops.subtract(alone, _through(shown, _DOUBLE)), _NONZERO)


def _around(boxes: Iterable[Bounds]) -> Bounds:
    """The smallest rectangle that holds `boxes`."""
    lefts, tops, rights, bottoms = zip(*boxes, strict=True)
    return min(lefts), min(tops), max(rights), max(bottoms)


def bounds_of(texts: Iterable[Text]) -> Bounds:
    """The smallest rectangle that holds the own text of all of `texts`."""
    return _around(text.bounds for text in texts)


def part(image: Image.Image, clip: Bounds, inner: Bounds) -> Image.Image:
    """The pixels of `inner` in `image`, a picture of the part `clip` of the page."""
    left, top = clip[0], clip[1]
    return image.crop(
        (inner[0] - left, inner[1] - top, inner[2] - left, inner[3] - top)
    )


def read_texts(
    found: list[dict[str, Any]], elements: list[Element], page: Image.Image
) -> list[Text]:
    """The texts the cover script `found`, in document order, without those whose
    own text has no pixel on `page`.

    The boxes of the own text are the ones the Capture holds for the element,
    rounded outwards and clamped to the page.
    """
    texts: list[Text] = []
    for entry in found:
        index: int = entry["index"]
        boxes = [
            box
            for box in (
                vision.bounds(page, own, 0) for own in elements[index].own_text_boxes
            )
            if box[0] < box[2] and box[1] < box[3]
        ]
        if not boxes:
            continue
        texts.append(
            Text(
                index=index,
                ancestors=frozenset(entry["ancestors"]),
                region=vision.bounds(page, Box.model_validate(entry["region"]), 0),
                layers=tuple(entry["layers"]),
                boxes=boxes,
                bounds=_around(boxes),
            )
        )
    return texts


def assign_channels(texts: list[Text]) -> int:
    """Give each text a round and a channel, so that two texts whose own-text boxes
    cross never share both; returns how many rounds that takes.

    A round is one pair of screenshots, which tells three texts painted over each
    other apart, one on each channel. Greedy, in document order.
    """
    # Only texts with a box in the same cell can cross.
    cells: dict[tuple[int, int], dict[int, list[Bounds]]] = {}
    for place, text in enumerate(texts):
        for box in text.boxes:
            for column in range(box[0] // _CELL_PX, (box[2] - 1) // _CELL_PX + 1):
                for row in range(box[1] // _CELL_PX, (box[3] - 1) // _CELL_PX + 1):
                    cells.setdefault((column, row), {}).setdefault(place, []).append(
                        box
                    )
    crossing: list[set[int]] = [set() for _ in texts]
    for members in cells.values():
        for one, boxes in members.items():
            for other, others in members.items():
                if (
                    one < other
                    and other not in crossing[one]
                    and any(_crosses(box, across) for box in boxes for across in others)
                ):
                    crossing[one].add(other)
                    crossing[other].add(one)
    colors: list[int] = []
    for place in range(len(texts)):
        taken = {colors[other] for other in crossing[place] if other < place}
        colors.append(next(color for color in itertools.count() if color not in taken))
    for text, color in zip(texts, colors, strict=True):
        text.round, text.channel = divmod(color, 3)
    return max(colors, default=-1) // 3 + 1


def ink_layers(on: Image.Image, off: Image.Image) -> Layers:
    """The ink of the glyphs marked on each channel: what `on`, a screenshot with
    them in the colour of their channel, has over `off`, the same with them in
    black. Whatever else is painted is in both and leaves nothing.
    """
    red, green, blue = ImageChops.subtract(on, off).split()
    return red, _through(green, _GREEN), blue


def may_be_covered(text: Text, glyphs: Layers, painted: Layers) -> bool:
    """Whether `text` can have enough Hidden ink to be reported: phase 1.

    `glyphs` is the ink of the texts of its round on a page where only their
    glyphs are painted, `painted` their ink on the page as it is. The ink of the
    text that is lost between the two is hidden by something, its Silent layers
    included, and where the glyphs of another text of the round lie in its boxes
    they may hide ink of it in both. The two together are never less than its
    Hidden ink, since its glyphs alone are never less than its Text ink.
    """
    inside = _own_text(text)
    alone = [layer.crop(text.bounds) for layer in glyphs]
    mine = alone[text.channel]
    ink = ImageChops.darker(_through(mine, _IS_TEXT), inside)
    lost = _count(
        ImageChops.darker(ink, _unseen(mine, painted[text.channel].crop(text.bounds)))
    )
    others = _through(
        ImageChops.lighter(
            alone[(text.channel + 1) % 3], alone[(text.channel + 2) % 3]
        ),
        _IS_OTHER,
    )
    collided = _count(
        ImageChops.darker(ImageChops.darker(others, inside), ImageChops.invert(ink))
    )
    return lost + collided > 0 and (
        lost + collided
    ) * 100 >= config.OVERLAP_MIN_HIDDEN_PERCENT * _count(ink)


def groups(candidates: list[Text]) -> list[list[Text]]:
    """`candidates` in groups whose members can each be painted alone in the same
    screenshot: none is inside another, and nothing one of them shows touches the
    own text of another. Greedy, in document order.
    """
    # ponytail: what a text shows is taken to be inside its region. A
    # pseudo-element of one member positioned over the own text of another is
    # not, and that text is measured with less Text ink than it has; give a text
    # that shows a positioned pseudo-element a group of its own if it happens.
    found: list[list[Text]] = []
    for text in candidates:
        for group in found:
            if not any(
                text.index in other.ancestors
                or other.index in text.ancestors
                or _crosses(text.region, other.bounds)
                or _crosses(other.region, text.bounds)
                for other in group
            ):
                group.append(text)
                break
        else:
            found.append([text])
    return found


def hidden_ink(
    text: Text, alone: Image.Image, painted: Image.Image, layered: Image.Image
) -> tuple[int, int, Image.Image]:
    """The Text ink and the Hidden ink of `text` in pixels, and where the Hidden
    ink is: a mask of its bounds.

    The three pictures are of its bounds and hold the ink of its own text:
    `alone` with only the text and what is inside it painted, `painted` on the
    page as it is and `layered` with the text and its Silent layers painted.
    """
    # ponytail: the text is cut out whole, from its first box to its last. One
    # with a text node at the top of a page and another at the bottom costs
    # pixel work on all that is between them; work box by box if it gets slow.
    ink = ImageChops.darker(_through(alone, _IS_TEXT), _own_text(text))
    # Unseen on the page, and not because of a Silent layer.
    hidden = ImageChops.darker(
        ImageChops.darker(ink, _unseen(alone, painted)),
        ImageChops.invert(_unseen(alone, layered)),
    )
    return _count(ink), _count(hidden), hidden


def runs(mask: Image.Image, origin: tuple[int, int]) -> list[tuple[int, int, int]]:
    """The set pixels of `mask` as runs along its rows, in page coordinates: the
    row, where the run starts and where it ends, the end not included. `origin`
    is where the first pixel of the mask is on the page.
    """
    left, top = origin
    width = mask.width
    data = mask.tobytes()
    found: list[tuple[int, int, int]] = []
    for row in range(mask.height):
        line = data[row * width : (row + 1) * width]
        start = line.find(b"\xff")
        while start >= 0:
            end = line.find(b"\x00", start)
            if end < 0:
                end = width
            found.append((top + row, left + start, left + end))
            start = line.find(b"\xff", end)
    return found


def hit_step(pixels: int) -> int:
    """How far apart, along a row and between rows, the pixels to hit test are
    taken so that `pixels` of them give at most `HIT_TEST_MAX` tests.
    """
    return max(1, math.ceil(math.sqrt(pixels / config.HIT_TEST_MAX)))
