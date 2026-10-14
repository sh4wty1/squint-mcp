"""The tokens of a Capture: the Terms of `extract_tokens` as code. No browser
code here."""

from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from squint_mcp.models import Capture, Element


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


def _family[T](tokens: list[T]) -> Family[T]:
    return Family(total=len(tokens), tokens=tokens)


def _is_read(element: Element) -> bool:
    """Whether an element is a Read element: one that paints a box."""
    return element.box.w > 0 and element.box.h > 0


def extract(capture: Capture) -> Tokens:
    """Read the Tokens of the elements a Capture holds."""
    read = [element for element in capture.elements if _is_read(element)]
    return Tokens(
        elements=len(read),
        colors=_family([]),
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
