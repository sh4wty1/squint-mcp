"""The Capture and the data it carries. No browser code here (ADR-0002)."""

from dataclasses import dataclass
from typing import Literal

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

    tag: str
    """The local name of the element, in lower case for an HTML one."""
    box: Box
    box_model: BoxModel
    computed: dict[str, str]
    text: str
    """An excerpt of the text content, whitespace collapsed."""
    own_text: bool
    """Whether a non-whitespace text node is a direct child."""
    own_text_boxes: list[Box]
    """The boxes, as painted and in page coordinates, of the text nodes that are
    direct children."""
    own_text_right: float | None
    """The right edge, as painted and in page coordinates, of the text nodes that
    are direct children; None when they paint no box."""
    opacity: float
    """The element's opacity multiplied by that of every ancestor."""
    scroll_width: int
    client_width: int
    selector: str
    """Unique on the page, open shadow trees included."""


@dataclass(frozen=True)
class Capture:
    """A stabilized snapshot of one page at one viewport: DOM/CSS data plus pixels."""

    viewport: Viewport
    stabilized: bool
    elements: list[Element]
    """The elements matched by the selector the Capture was taken for, in
    document order."""
    scroll_width: int
    """How wide the page scrolls, in CSS pixels. The pixels can be wider: they
    also hold what a `body` that is its own scroll container clips."""
    pixels: Image.Image
    """The full page in RGB, one image pixel per CSS pixel."""
    background: Image.Image
    """The full page in RGB with no text painted."""
    ink: Image.Image
    """How much text ink each pixel gets, 0 to 255, in mode L."""


Severity = Literal["critical", "major", "minor", "info"]
Category = Literal["visual-bug", "a11y", "consistency", "ux", "responsive"]


class Evidence(BaseModel):
    """What backs a Finding: the styles that explain it and what was measured."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    computed: dict[str, str]
    measured: dict[str, int | float | str]
    crop_index: int | None = None
    """Index of the Finding's crop among the images of the response, if it has one."""


class Finding(BaseModel):
    """One problem a Check found on one element of a Capture."""

    check: str
    category: Category
    severity: Severity
    message: str
    selector: str
    text: str
    box: Box
    viewport: Viewport
    evidence: Evidence
    suggestion: str | None = None
    source: str | None = None
