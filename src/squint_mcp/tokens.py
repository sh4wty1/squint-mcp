"""The tokens of a Capture: the Terms of `extract_tokens` as code. No browser
code here."""

from collections import Counter
from collections.abc import Iterable, Iterator
from typing import Literal

from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from squint_mcp import color
from squint_mcp.models import Capture, Edges, Element


class Variant[V: (float, str)](BaseModel):
    """One Value of a Group, with its own Uses."""

    value: V
    uses: int


class ColorRoles(BaseModel):
    text: int
    background: int
    border: int


class SpacingRoles(BaseModel):
    margin: int
    padding: int
    gap: int


class ColorToken(BaseModel):
    value: str
    """`#rrggbb`, or `#rrggbbaa` for a colour that is not opaque."""
    uses: int
    roles: ColorRoles
    variants: list[Variant[str]]


class TextToken(BaseModel):
    value: str
    uses: int


class NumberToken(BaseModel):
    value: float
    uses: int


class LengthToken(BaseModel):
    value: float
    """In px."""
    uses: int
    variants: list[Variant[float]]


class SpacingToken(BaseModel):
    value: float
    """In px."""
    uses: int
    roles: SpacingRoles
    variants: list[Variant[float]]


class RadiusToken(BaseModel):
    value: str
    """The computed text of a corner: `4px`, `50%`, `10px 20px`."""
    uses: int
    variants: list[Variant[str]]


class ShadowToken(BaseModel):
    kind: Literal["box", "text"]
    value: str
    """The whole computed text of the property."""
    uses: int


class Family[T](BaseModel):
    total: int
    tokens: list[T]


class Typography(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    families: Family[TextToken]
    sizes: Family[LengthToken]
    weights: Family[NumberToken]
    line_heights: Family[LengthToken]


class Tokens(BaseModel):
    """The eight Families of a Capture."""

    elements: int
    """How many Read elements the Tokens were read from."""
    colors: Family[ColorToken]
    typography: Typography
    spacing: Family[SpacingToken]
    radii: Family[RadiusToken]
    shadows: Family[ShadowToken]


type Uses[V] = dict[V, Counter[str]]
"""How many Read elements have each Value of a Family, by Role."""


def _use[V](uses: Uses[V], role: str, values: Iterable[V]) -> None:
    """Count what one element has in one Role: a Value it has on several sides
    is one Use."""
    for value in set(values):
        uses.setdefault(value, Counter())[role] += 1


def _ranked[V: (float, str)](uses: Uses[V]) -> list[V]:
    """The Values in Rank order: by Uses, most first, then by Value."""
    return sorted(uses, key=lambda value: (-uses[value].total(), value))


def _family[T](tokens: list[T]) -> Family[T]:
    return Family(total=len(tokens), tokens=tokens)


def _sides(edges: Edges) -> list[tuple[str, float]]:
    return [
        ("top", edges.top),
        ("right", edges.right),
        ("bottom", edges.bottom),
        ("left", edges.left),
    ]


def _hexes(texts: Iterable[str]) -> Iterator[str]:
    """The colour Values among computed colours: those of alpha above 0."""
    for text in texts:
        parsed = color.parse(text)
        if parsed is None:
            raise ToolError(f'Unsupported colour "{text}".')
        if parsed[3] > 0:
            yield color.to_hex(parsed)


def _colors(read: list[Element]) -> Family[ColorToken]:
    uses: Uses[str] = {}
    for element in read:
        computed = element.computed
        if _paints_text(element):
            _use(uses, "text", _hexes([computed["color"]]))
        _use(uses, "background", _hexes([computed["background-color"]]))
        # A side with no border still computes a colour: the width decides.
        borders = (
            computed[f"border-{side}-color"]
            for side, width in _sides(element.box_model.border)
            if width > 0
        )
        _use(uses, "border", _hexes(borders))
    tokens: list[ColorToken] = []
    for value in _ranked(uses):
        roles = uses[value]
        token = ColorToken(
            value=value,
            uses=roles.total(),
            roles=ColorRoles(
                text=roles["text"],
                background=roles["background"],
                border=roles["border"],
            ),
            variants=[Variant[str](value=value, uses=roles.total())],
        )
        tokens.append(token)
    return _family(tokens)


def _is_read(element: Element) -> bool:
    """Whether an element is a Read element: one that paints a box."""
    return element.box.w > 0 and element.box.h > 0


def _paints_text(element: Element) -> bool:
    """Whether an element has Painted text: own text that paints a box."""
    return element.own_text and bool(element.own_text_boxes)


def extract(capture: Capture) -> Tokens:
    """Read the Tokens of the elements a Capture holds."""
    read = [element for element in capture.elements if _is_read(element)]
    return Tokens(
        elements=len(read),
        colors=_colors(read),
        typography=Typography(
            families=_family([]),
            sizes=_family([]),
            weights=_family([]),
            line_heights=_family([]),
        ),
        spacing=_family([]),
        radii=_family([]),
        shadows=_family([]),
    )
