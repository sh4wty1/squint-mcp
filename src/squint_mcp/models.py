"""The Capture and the data it carries. No browser code here (ADR-0002)."""

from dataclasses import dataclass

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Viewport(BaseModel):
    width: int = Field(ge=1)
    height: int = Field(ge=1)


class Box(BaseModel):
    """A border box in CSS pixels, in page coordinates."""

    x: float
    y: float
    w: float
    h: float


class Edges(BaseModel):
    top: float
    right: float
    bottom: float
    left: float


class Size(BaseModel):
    w: float
    h: float


class BoxModel(BaseModel):
    margin: Edges
    border: Edges
    padding: Edges
    content: Size


class Element(BaseModel):
    """One element as collected inside the page."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    box: Box
    box_model: BoxModel
    computed: dict[str, str]


@dataclass(frozen=True)
class Capture:
    """A stabilized snapshot of one page at one viewport: DOM/CSS data plus pixels."""

    viewport: Viewport
    stabilized: bool
    elements: list[Element]
    """The elements matched by the selector the Capture was taken for."""
    pixels: Image.Image
    """The full page in RGB, one image pixel per CSS pixel."""
