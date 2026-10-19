"""`extract_tokens` through the MCP tool boundary, against real Chromium."""

import time
from typing import Any

import anyio
import pytest
from helpers import FIXTURES, fixture_url, texts
from mcp import Client
from mcp.types import CallToolResult, TextContent, Tool

from squint_mcp import config

pytestmark = pytest.mark.anyio

PAGE = "tokens-page.html"
USED = "tokens-used.html"
GROUPS = "tokens-groups.html"
DEFAULT = "tokens-default.html"
SCOPE = "tokens-scope.html"
LIMIT = "tokens-limit.html"
VIEWPORT = "tokens-viewport.html"
BORDERS = "tokens-borders.html"
TWENTY = [value * 10 for value in range(1, 21)]


async def tokens_tool(client: Client) -> Tool:
    (tool,) = (
        t for t in (await client.list_tools()).tools if t.name == "extract_tokens"
    )
    return tool


async def call(client: Client, name: str, **arguments: Any) -> CallToolResult:
    """Call the tool on the fixture `name`, or on `name` itself when it is a url."""
    url = name if "://" in name else fixture_url(name)
    return await client.call_tool("extract_tokens", {"url": url, **arguments})


async def extract(client: Client, name: str, **arguments: Any) -> dict[str, Any]:
    """Call the tool on a fixture and return its structured content, failing on
    a tool error and on a Token whose sums do not hold."""
    result = await call(client, name, **arguments)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    assert_sums_hold(result.structured_content)
    for family in families(result.structured_content):
        assert len(family["tokens"]) <= 20
    return result.structured_content


async def fail(client: Client, name: str, **arguments: Any) -> str:
    """Call the tool on a fixture and return the message it fails with: a
    failure is an error with no structured content."""
    result = await call(client, name, **arguments)
    assert result.is_error is True
    assert result.structured_content is None
    (text,) = texts(result)
    # The SDK names the tool before the message of the ToolError.
    prefix = "Error executing tool extract_tokens: "
    assert text.startswith(prefix), text
    return text.removeprefix(prefix)


def assert_sums_hold(result: dict[str, Any]) -> None:
    """The `uses` of every Token are those of its variants, its `value` that of
    the first of them, and where it has Roles its `uses` are theirs."""
    typography = result["typography"]
    for family in (
        result["colors"],
        typography["sizes"],
        typography["lineHeights"],
        result["spacing"],
        result["radii"],
    ):
        for token in family["tokens"]:
            variants = token["variants"]
            assert token["uses"] == sum(variant["uses"] for variant in variants), token
            assert token["value"] == variants[0]["value"], token
    for family in (result["colors"], result["spacing"]):
        for token in family["tokens"]:
            assert token["uses"] == sum(token["roles"].values()), token


def families(result: dict[str, Any]) -> list[dict[str, Any]]:
    """The eight Families of a result."""
    typography = result["typography"]
    return [
        result["colors"],
        typography["families"],
        typography["sizes"],
        typography["weights"],
        typography["lineHeights"],
        result["spacing"],
        result["radii"],
        result["shadows"],
    ]


def rows(family: dict[str, Any], *fields: str) -> list[tuple[Any, ...]]:
    """Each Token of a Family as the tuple of `fields`, a Role written
    `roles.<role>` as the criteria write it."""

    def read(token: Any, field: str) -> Any:
        for key in field.split("."):
            token = token[key]
        return token

    return [tuple(read(token, field) for field in fields) for token in family["tokens"]]


def held(family: dict[str, Any], value: Any) -> dict[str, Any]:
    """The Token of a Family that "holds" `value`: the one whose `value` it is."""
    tokens = [token for token in family["tokens"] if token["value"] == value]
    assert len(tokens) == 1, (value, rows(family, "value"))
    return tokens[0]


def values(family: dict[str, Any]) -> list[Any]:
    """Every `value` of a Family, of a Token or of a variant: the Family "does
    not hold" a value that is none of them."""
    found: list[Any] = []
    for token in family["tokens"]:
        found.append(token["value"])
        found.extend(variant["value"] for variant in token.get("variants", []))
    return found


async def test_extract_tokens_is_listed_with_its_hints_and_its_schemas(
    client: Client,
) -> None:
    tool = await tokens_tool(client)
    assert tool.annotations is not None
    assert tool.annotations.read_only_hint is True
    assert tool.annotations.open_world_hint is True
    assert tool.output_schema is not None

    schema = tool.input_schema
    properties = schema["properties"]
    assert set(properties) == {"url", "scope", "viewport", "storageState"}
    assert schema["required"] == ["url"]
    assert properties["url"]["type"] == "string"

    def options(name: str) -> dict[str, dict[str, Any]]:
        """What an optional argument takes, by JSON type."""
        resolved: dict[str, dict[str, Any]] = {}
        for option in properties[name]["anyOf"]:
            if "$ref" in option:
                option = schema["$defs"][option["$ref"].removeprefix("#/$defs/")]
            resolved[option["type"]] = option
        return resolved

    assert set(options("scope")) == {"string", "null"}
    viewport = options("viewport")
    assert set(viewport) == {"object", "null"}
    sides = viewport["object"]["properties"]
    assert set(sides) == {"width", "height"}
    assert sides["width"]["minimum"] == 1
    assert sides["height"]["minimum"] == 1


async def test_result_tells_the_call_the_elements_read_and_a_total_per_family(
    client: Client,
) -> None:
    result = await extract(client, PAGE)
    assert result["viewport"] == {"width": 1440, "height": 900}
    assert result["stabilized"] is True
    assert result["scope"] is None
    # `html`, `body` and the six elements of the page: those of `head` have no box.
    assert result["elements"] == 8
    for family in families(result):
        assert family["total"] == len(family["tokens"])


async def test_result_is_one_text_block_and_no_image(client: Client) -> None:
    result = await call(client, PAGE)
    assert result.is_error is False, texts(result)
    (block,) = result.content
    assert isinstance(block, TextContent)


async def test_colors_are_counted_by_role_and_come_in_rank_order(
    client: Client,
) -> None:
    colors = (await extract(client, PAGE))["colors"]
    fields = ("value", "uses", "roles.text", "roles.background", "roles.border")
    # Two Tokens of 2 Uses and two of 1: each pair in the order of its text.
    assert rows(colors, *fields) == [
        ("#333333", 3, 3, 0, 0),
        ("#1a73e8", 2, 1, 1, 0),
        ("#ffffff", 2, 1, 1, 0),
        ("#cccccc", 1, 0, 0, 1),
        ("#eeeeee", 1, 0, 1, 0),
    ]
    # No two colours of the page are Near: each Token is its own one variant.
    assert [token["variants"] for token in colors["tokens"]] == [
        [{"value": "#333333", "uses": 3}],
        [{"value": "#1a73e8", "uses": 2}],
        [{"value": "#ffffff", "uses": 2}],
        [{"value": "#cccccc", "uses": 1}],
        [{"value": "#eeeeee", "uses": 1}],
    ]


async def test_font_families_are_counted_on_painted_text(client: Client) -> None:
    typography = (await extract(client, PAGE))["typography"]
    # Five of the eight elements have text of their own.
    assert rows(typography["families"], "value", "uses") == [("Arial, sans-serif", 5)]


async def test_font_sizes_come_by_value(client: Client) -> None:
    typography = (await extract(client, PAGE))["typography"]
    assert rows(typography["sizes"], "value", "uses") == [(14, 3), (16, 1), (32, 1)]


async def test_font_weights_come_by_value_not_by_uses(client: Client) -> None:
    typography = (await extract(client, PAGE))["typography"]
    assert rows(typography["weights"], "value", "uses") == [(400, 2), (700, 3)]


async def test_line_heights_come_by_value(client: Client) -> None:
    typography = (await extract(client, PAGE))["typography"]
    line_heights = typography["lineHeights"]
    assert rows(line_heights, "value", "uses") == [(20, 3), (24, 1), (40, 1)]


async def test_spacings_are_counted_by_role_and_come_by_value(client: Client) -> None:
    spacing = (await extract(client, PAGE))["spacing"]
    fields = ("value", "uses", "roles.margin", "roles.padding", "roles.gap")
    # 16 has the most Uses and comes second; the padding of `#card` on four sides
    # and that of `#button` on two are one Use each, as the two axes of a gap are.
    assert rows(spacing, *fields) == [
        (8, 2, 0, 1, 1),
        (16, 3, 1, 2, 0),
        (24, 1, 1, 0, 0),
    ]


async def test_radii_are_counted_once_for_four_equal_corners(client: Client) -> None:
    radii = (await extract(client, PAGE))["radii"]
    # The six elements with no radius have corners of `0px`.
    assert rows(radii, "value", "uses") == [("4px", 1), ("8px", 1)]


async def test_a_box_shadow_is_one_token_of_its_whole_text(client: Client) -> None:
    shadows = (await extract(client, PAGE))["shadows"]
    # The seven elements with no shadow compute `none`.
    assert rows(shadows, "kind", "value", "uses") == [
        ("box", "rgba(0, 0, 0, 0.2) 0px 1px 3px 0px", 1)
    ]


async def test_summary_counts_each_family_and_the_elements(client: Client) -> None:
    result = await call(client, PAGE)
    assert result.is_error is False, texts(result)
    block = result.content[0]
    assert isinstance(block, TextContent)
    assert block.text == (
        "Tokens: colors 5, font families 1, font sizes 3, font weights 2, "
        "line heights 3, spacing 3, radii 2, shadows 1; elements 8; stabilized."
    )


async def test_two_calls_with_the_same_arguments_return_equal_content(
    client: Client,
) -> None:
    first = await extract(client, PAGE)
    second = await extract(client, PAGE)
    assert first == second


async def test_a_text_color_is_counted_where_the_text_is_not_where_it_is_set(
    client: Client,
) -> None:
    colors = (await extract(client, USED))["colors"]
    # `#inherit` sets the colour and has no text of its own: its child paints it.
    token = held(colors, "#aa0000")
    assert (token["uses"], token["roles"]["text"]) == (1, 1)


async def test_a_text_color_is_the_fill_of_the_text(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    assert held(colors, "#222222")["roles"]["text"] == 1
    assert "#111111" not in values(colors)


async def test_a_background_of_alpha_zero_is_no_color(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    assert [value for value in values(colors) if value.startswith("#008080")] == []


async def test_a_transparent_text_fill_is_no_color(client: Client) -> None:
    found = values((await extract(client, USED))["colors"])
    assert [value for value in found if value.startswith("#445566")] == []
    assert [value for value in found if len(value) == 9 and value.endswith("00")] == []


async def test_a_color_that_is_not_opaque_has_its_alpha_rounded_half_up(
    client: Client,
) -> None:
    colors = (await extract(client, USED))["colors"]
    # An alpha of 0.5 is 127.5 of 255.
    assert held(colors, "#00000080")["roles"]["background"] == 1


async def test_a_border_color_is_counted_only_on_a_side_that_has_a_width(
    client: Client,
) -> None:
    colors = (await extract(client, USED))["colors"]
    token = held(colors, "#0000aa")
    assert (token["uses"], token["roles"]["border"]) == (1, 1)
    # The three sides with no border compute the `color` of `#edge`.
    assert "#00aa00" not in values(colors)


async def test_each_side_of_a_border_gives_its_own_color(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    for value in ("#800000", "#008000", "#000080", "#808000"):
        assert held(colors, value)["roles"]["border"] == 1


async def test_a_default_button_gives_no_border_color(client: Client) -> None:
    # It computes `outset rgb(0, 0, 0)`; the theme paints it `#767676`.
    colors = (await extract(client, BORDERS))["colors"]
    assert "#000000" not in values(colors)


@pytest.mark.parametrize("value", ["#aa0000", "#00aa00", "#0000aa", "#aa00aa"])
async def test_a_shaded_border_gives_no_color(client: Client, value: str) -> None:
    colors = (await extract(client, BORDERS))["colors"]
    assert value not in values(colors)


async def test_only_the_shaded_sides_of_a_border_are_left_out(client: Client) -> None:
    colors = (await extract(client, BORDERS))["colors"]
    token = held(colors, "#112233")
    assert (token["uses"], token["roles"]["border"]) == (1, 1)
    assert "#445566" not in values(colors)


@pytest.mark.parametrize("value", ["#cc6600", "#0066cc", "#66cc00", "#cc0066"])
async def test_a_border_of_any_other_style_gives_its_color(
    client: Client, value: str
) -> None:
    colors = (await extract(client, BORDERS))["colors"]
    token = held(colors, value)
    assert (token["uses"], token["roles"]["border"]) == (1, 1)


async def test_the_description_says_a_shaded_border_is_not_counted(
    client: Client,
) -> None:
    description = " ".join(((await tokens_tool(client)).description or "").split())
    assert "`outset`, `inset`, `groove` or `ridge` is not counted" in description


async def test_a_color_in_the_srgb_notation_is_read(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    # `color(srgb 0.2 0.4 0.6)`: 51, 102 and 153 of 255.
    assert ("#336699",) in rows(colors, "value")


async def test_a_color_outside_srgb_is_clipped_to_it(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    # The red of display-p3 has, in sRGB, a red above 1 and a green and a blue
    # below 0.
    assert ("#ff0000",) in rows(colors, "value")


async def test_own_text_that_paints_no_box_is_not_painted_text(client: Client) -> None:
    result = await extract(client, USED)
    typography = result["typography"]
    # `#mute`: a box of 100px by 20px whose text, of font size 0, paints no box.
    for name in ("families", "sizes", "weights", "lineHeights"):
        for value in ("Courier, monospace", 0, 700, 37):
            assert value not in values(typography[name]), (name, value)
    assert "#abcdef" not in values(result["colors"])
    for value in values(result["shadows"]):
        assert "3px 3px 3px" not in value


async def test_type_values_are_counted_where_the_text_is_not_where_they_are_set(
    client: Client,
) -> None:
    typography = (await extract(client, USED))["typography"]
    # `#big` sets a font and has no text of its own: its child sets another.
    for name in ("families", "sizes", "weights", "lineHeights"):
        for value in (40, 900, 50, "Georgia, serif"):
            assert value not in values(typography[name]), name
    assert (12,) in rows(typography["sizes"], "value")


async def test_a_line_height_of_normal_is_no_value(client: Client) -> None:
    typography = (await extract(client, USED))["typography"]
    sizes, line_heights = typography["sizes"], typography["lineHeights"]
    assert (13,) in rows(sizes, "value")
    # Every text of the page but that of `#normal` has a line height in px.
    assert sum(uses for (uses,) in rows(line_heights, "uses")) == (
        sum(uses for (uses,) in rows(sizes, "uses")) - 1
    )


async def test_a_line_height_is_read_as_the_length_it_computes_to(
    client: Client,
) -> None:
    typography = (await extract(client, USED))["typography"]
    # `#ratio`: a line height of 1.5 on a font size of 20px.
    assert (30,) in rows(typography["lineHeights"], "value")


async def test_each_side_of_a_margin_gives_its_own_spacing(client: Client) -> None:
    spacing = (await extract(client, USED))["spacing"]
    for value in (51, 53, 55, 57):
        token = held(spacing, value)
        assert (token["uses"], token["roles"]["margin"]) == (1, 1)


async def test_each_side_of_a_padding_gives_its_own_spacing(client: Client) -> None:
    spacing = (await extract(client, USED))["spacing"]
    for value in (61, 63, 65, 67):
        token = held(spacing, value)
        assert (token["uses"], token["roles"]["padding"]) == (1, 1)


async def test_a_margin_of_auto_is_no_spacing(client: Client) -> None:
    spacing = (await extract(client, USED))["spacing"]
    # `#centered` is 200px wide in a `body` of 1440px: 620px is laid out on
    # each side of it.
    assert 620 not in values(spacing)


async def test_a_negative_margin_is_no_spacing(client: Client) -> None:
    found = values((await extract(client, USED))["spacing"])
    assert [value for value in found if value <= 0] == []
    assert 71 not in found


async def test_each_axis_of_a_gap_gives_its_own_spacing(client: Client) -> None:
    spacing = (await extract(client, USED))["spacing"]
    for value in (81, 83):
        assert held(spacing, value)["roles"]["gap"] == 1


async def test_a_gap_is_counted_on_each_display_that_lays_one_out(
    client: Client,
) -> None:
    spacing = (await extract(client, USED))["spacing"]
    # `inline-flex`, `grid` and `inline-grid`, in turn.
    for value in (85, 87, 89):
        token = held(spacing, value)
        assert (token["uses"], token["roles"]["gap"]) == (1, 1)


async def test_the_gap_of_a_block_is_no_spacing(client: Client) -> None:
    spacing = (await extract(client, USED))["spacing"]
    assert 91 not in values(spacing)


async def test_each_corner_gives_its_own_radius_and_a_zero_corner_none(
    client: Client,
) -> None:
    radii = (await extract(client, USED))["radii"]
    for value in ("41px", "43px", "45px", "47px"):
        assert held(radii, value)["uses"] == 1
    # Every other box of the page has corners of `0px`.
    assert "0px" not in values(radii)


async def test_radii_that_are_not_one_length_come_after_those_that_are(
    client: Client,
) -> None:
    radii = (await extract(client, USED))["radii"]
    # `#oval` and `#round`, in the order of their texts: the four corners of
    # `#corners`, each one px length, come before both.
    assert rows(radii, "value", "uses")[-2:] == [("10px 20px", 1), ("50%", 1)]


async def test_a_text_shadow_is_counted_where_the_text_is_not_where_it_is_set(
    client: Client,
) -> None:
    shadows = (await extract(client, USED))["shadows"]
    # `#glow` sets the shadow and has no text of its own: its child paints it.
    fields = ("kind", "value", "uses")
    assert [row for row in rows(shadows, *fields) if row[0] == "text"] == [
        ("text", "rgb(0, 0, 0) 1px 1px 2px", 1)
    ]


async def test_a_shadow_of_two_layers_is_one_token(client: Client) -> None:
    shadows = (await extract(client, USED))["shadows"]
    fields = ("kind", "value", "uses")
    assert [row for row in rows(shadows, *fields) if row[0] == "box"] == [
        ("box", "rgb(0, 0, 0) 0px 1px 2px 0px, rgb(0, 0, 0) 0px 4px 8px 0px", 1)
    ]


async def test_an_element_that_is_not_visible_is_not_read(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    assert "#aa00aa" not in values(colors)


async def test_an_element_under_an_opacity_of_zero_is_not_read(client: Client) -> None:
    colors = (await extract(client, USED))["colors"]
    # `#faded-child` has no opacity of its own: that of `#faded` hides it.
    assert "#00aaaa" not in values(colors)


async def test_an_element_that_paints_no_box_is_not_read(client: Client) -> None:
    result = await extract(client, USED)
    found = values(result["colors"])
    # `#none`, `#flat-w` and `#flat-h`, in turn.
    for value in ("#abcd01", "#abcd02", "#abcd03"):
        assert value not in found
    # `html`, `body` and 30 of the 36 elements of `body`: all but the three
    # above, `#hidden`, `#faded` and `#faded-child`.
    assert result["elements"] == 32


async def test_the_families_of_a_page_come_whole_and_in_their_order(
    client: Client,
) -> None:
    result = await extract(client, USED)
    typography = result["typography"]
    # Rank order: the colour of the four texts that share one, then the ten of
    # 1 Use by their text, where a digit comes before a letter.
    fields = ("value", "uses", "roles.text", "roles.background", "roles.border")
    assert rows(result["colors"], *fields) == [
        ("#333333", 4, 4, 0, 0),
        ("#00000080", 1, 0, 1, 0),
        ("#000080", 1, 0, 0, 1),
        ("#0000aa", 1, 0, 0, 1),
        ("#008000", 1, 0, 0, 1),
        ("#222222", 1, 1, 0, 0),
        ("#336699", 1, 0, 1, 0),
        ("#800000", 1, 0, 0, 1),
        ("#808000", 1, 0, 0, 1),
        ("#aa0000", 1, 1, 0, 0),
        ("#ff0000", 1, 0, 1, 0),
    ]
    # Rank order: Arial on five of the seven texts, then the family of `#clip`
    # and that of `#fill` by their text, where a quote comes before a letter.
    assert rows(typography["families"], "value", "uses") == [
        ("Arial, sans-serif", 5),
        ('"Segoe UI", sans-serif', 1),
        ("Verdana, sans-serif", 1),
    ]
    # By value: four of the seven texts are 14px on a line of 20px, and that of
    # `#normal` has no line height.
    assert rows(typography["sizes"], "value", "uses") == [
        (12, 1),
        (13, 1),
        (14, 4),
        (20, 1),
    ]
    assert rows(typography["weights"], "value", "uses") == [(400, 7)]
    assert rows(typography["lineHeights"], "value", "uses") == [
        (18, 1),
        (20, 4),
        (30, 1),
    ]
    fields = ("value", "uses", "roles.margin", "roles.padding", "roles.gap")
    assert rows(result["spacing"], *fields) == [
        (51, 1, 1, 0, 0),
        (53, 1, 1, 0, 0),
        (55, 1, 1, 0, 0),
        (57, 1, 1, 0, 0),
        (61, 1, 0, 1, 0),
        (63, 1, 0, 1, 0),
        (65, 1, 0, 1, 0),
        (67, 1, 0, 1, 0),
        (81, 1, 0, 0, 1),
        (83, 1, 0, 0, 1),
        (85, 1, 0, 0, 1),
        (87, 1, 0, 0, 1),
        (89, 1, 0, 0, 1),
    ]
    # The four that are one px length, then the two others by their text.
    assert rows(result["radii"], "value", "uses") == [
        ("41px", 1),
        ("43px", 1),
        ("45px", 1),
        ("47px", 1),
        ("10px 20px", 1),
        ("50%", 1),
    ]
    assert rows(result["shadows"], "kind", "value", "uses") == [
        ("box", "rgb(0, 0, 0) 0px 1px 2px 0px, rgb(0, 0, 0) 0px 4px 8px 0px", 1),
        ("text", "rgb(0, 0, 0) 1px 1px 2px", 1),
    ]


async def test_near_colors_are_one_token_whose_value_is_the_most_used(
    client: Client,
) -> None:
    colors = (await extract(client, GROUPS))["colors"]
    # `#1a78e8` comes first in the document, on two boxes and a text: ΔE2000
    # 1.8554 from `#1a73e8`, which has 4 Uses.
    token = held(colors, "#1a73e8")
    assert token["uses"] == 7
    assert token["roles"] == {"text": 1, "background": 6, "border": 0}
    assert token["variants"] == [
        {"value": "#1a73e8", "uses": 4},
        {"value": "#1a78e8", "uses": 3},
    ]


async def test_a_color_is_compared_with_the_representative_of_a_group_only(
    client: Client,
) -> None:
    colors = (await extract(client, GROUPS))["colors"]
    # ΔE2000 2.2280 from the Representative `#1a73e8`, 0.3724 from its variant
    # `#1a78e8`.
    token = held(colors, "#1a79e8")
    assert token["uses"] == 1
    assert token["variants"] == [{"value": "#1a79e8", "uses": 1}]


async def test_colors_of_another_alpha_are_not_near(client: Client) -> None:
    colors = (await extract(client, GROUPS))["colors"]
    # The colour of `#1a73e8` at an alpha of 0.5.
    token = held(colors, "#1a73e880")
    assert token["uses"] == 1
    assert token["variants"] == [{"value": "#1a73e880", "uses": 1}]


async def test_a_tie_in_uses_goes_to_the_lower_value_not_the_first_of_the_document(
    client: Client,
) -> None:
    colors = (await extract(client, GROUPS))["colors"]
    # `#858585` comes first in the document, on two boxes: ΔE2000 1.8620 from
    # `#808080`, on two boxes too.
    token = held(colors, "#808080")
    assert token["uses"] == 4
    assert token["variants"] == [
        {"value": "#808080", "uses": 2},
        {"value": "#858585", "uses": 2},
    ]


async def test_colors_rank_by_the_uses_of_their_whole_group(client: Client) -> None:
    colors = (await extract(client, GROUPS))["colors"]
    # `#ff8800` has 5 Uses, more than the 4 of `#1a73e8` alone and fewer than
    # the 7 of its Group; its Group opens before that of `#1a73e8`.
    assert rows(colors, "value", "uses") == [
        ("#333333", 8),
        ("#1a73e8", 7),
        ("#ff8800", 5),
        ("#808080", 4),
        ("#1a73e880", 1),
        ("#1a79e8", 1),
    ]


async def test_font_sizes_exactly_1px_apart_are_not_near(client: Client) -> None:
    typography = (await extract(client, GROUPS))["typography"]
    # 15px on one text, 16px on three, 16.5px, 16.75px, 17px on two, 17.75px.
    assert rows(typography["sizes"], "value", "uses") == [(15, 1), (16, 4), (17, 4)]


async def test_a_font_size_joins_the_nearest_group_not_the_most_used(
    client: Client,
) -> None:
    typography = (await extract(client, GROUPS))["typography"]
    # 16.75px is 0.75px from 16px, which has more Uses, and 0.25px from 17px.
    assert held(typography["sizes"], 17)["variants"] == [
        {"value": 17, "uses": 2},
        {"value": 16.75, "uses": 1},
        {"value": 17.75, "uses": 1},
    ]


async def test_a_font_size_as_near_two_groups_joins_the_first_opened(
    client: Client,
) -> None:
    typography = (await extract(client, GROUPS))["typography"]
    # 16.5px is 0.5px from 16px and from 17px: the Group of 16px, which has more
    # Uses, was opened first.
    assert held(typography["sizes"], 16)["variants"] == [
        {"value": 16, "uses": 3},
        {"value": 16.5, "uses": 1},
    ]


async def test_radii_that_are_not_one_length_are_never_near(client: Client) -> None:
    radii = (await extract(client, GROUPS))["radii"]
    # Two percentages half a percent apart, and two corners of two radii whose
    # first radius is half a pixel apart.
    for value in ("30%", "30.5%", "10px 20px", "10.5px 20px"):
        token = held(radii, value)
        assert token["uses"] == 1
        assert token["variants"] == [{"value": value, "uses": 1}]


async def test_spacings_less_than_1px_apart_are_one_token(client: Client) -> None:
    spacing = (await extract(client, GROUPS))["spacing"]
    token = held(spacing, 8)
    assert (token["uses"], token["roles"]["padding"]) == (3, 3)
    assert token["variants"] == [{"value": 8, "uses": 2}, {"value": 8.5, "uses": 1}]


async def test_radii_less_than_1px_apart_are_one_token(client: Client) -> None:
    radii = (await extract(client, GROUPS))["radii"]
    token = held(radii, "4px")
    assert token["uses"] == 3
    assert token["variants"] == [
        {"value": "4px", "uses": 2},
        {"value": "4.5px", "uses": 1},
    ]


async def test_line_heights_less_than_1px_apart_are_one_token(client: Client) -> None:
    typography = (await extract(client, GROUPS))["typography"]
    # Eight of the nine texts are on a line of 20px, `#s15` on one of 20.5px.
    (token,) = typography["lineHeights"]["tokens"]
    assert token["value"] == 20
    assert token["variants"][-1] == {"value": 20.5, "uses": 1}


async def test_the_families_of_a_page_of_near_values_come_whole_and_in_their_order(
    client: Client,
) -> None:
    result = await extract(client, GROUPS)
    typography = result["typography"]
    # Rank order of the Tokens, by the Uses of their Groups: the eight texts
    # in `#333333`, the Group of `#1a73e8`, the five boxes of `#ff8800` and the
    # Group of `#808080`, then two of 1 Use by their text, where a digit comes
    # before a letter.
    fields = ("value", "uses", "roles.text", "roles.background", "roles.border")
    assert rows(result["colors"], *fields) == [
        ("#333333", 8, 8, 0, 0),
        ("#1a73e8", 7, 1, 6, 0),
        ("#ff8800", 5, 0, 5, 0),
        ("#808080", 4, 0, 4, 0),
        ("#1a73e880", 1, 0, 1, 0),
        ("#1a79e8", 1, 0, 1, 0),
    ]
    assert rows(typography["families"], "value", "uses") == [("Arial, sans-serif", 9)]
    assert rows(typography["sizes"], "value", "uses") == [(15, 1), (16, 4), (17, 4)]
    assert rows(typography["weights"], "value", "uses") == [(400, 9)]
    assert rows(typography["lineHeights"], "value", "uses") == [(20, 9)]
    fields = ("value", "uses", "roles.margin", "roles.padding", "roles.gap")
    assert rows(result["spacing"], *fields) == [(8, 3, 0, 3, 0)]
    # The one Length, then the four others by their text, where a dot comes
    # before a letter and a percent sign before a dot.
    assert rows(result["radii"], "value", "uses") == [
        ("4px", 3),
        ("10.5px 20px", 1),
        ("10px 20px", 1),
        ("30%", 1),
        ("30.5%", 1),
    ]
    assert rows(result["shadows"], "kind", "value", "uses") == []


async def test_two_near_values_on_one_element_are_two_uses(client: Client) -> None:
    spacing = (await extract(client, DEFAULT))["spacing"]
    # `#mixed`: a padding of 40px at the top and the bottom, 40.5px at the sides.
    token = held(spacing, 40)
    assert token["uses"] == 2
    assert token["variants"] == [{"value": 40, "uses": 1}, {"value": 40.5, "uses": 1}]


async def test_a_margin_of_the_browser_stylesheet_is_counted(client: Client) -> None:
    spacing = (await extract(client, DEFAULT))["spacing"]
    # The page does not reset the margin of `body`.
    token = held(spacing, 8)
    assert (token["uses"], token["roles"]["margin"]) == (1, 1)


async def test_a_scope_reads_its_matches_and_what_is_under_them(
    client: Client,
) -> None:
    result = await extract(client, SCOPE, scope=".card")
    # The two cards share one colour; the three others of 1 Use come by their
    # text, where a digit comes before a letter.
    assert rows(result["colors"], "value", "uses") == [
        ("#00ff00", 2),
        ("#0000ff", 1),
        ("#00ffff", 1),
        ("#ffff00", 1),
    ]
    assert result["scope"] == ".card"


async def test_a_match_under_a_match_is_read_once(client: Client) -> None:
    result = await extract(client, SCOPE, scope=".card")
    # `#one`, `#one-child`, `#two`, `#inner`, `#host` and `#deep`.
    assert result["elements"] == 6
    assert held(result["colors"], "#ffff00")["uses"] == 1


async def test_no_scope_reads_the_whole_page(client: Client) -> None:
    result = await extract(client, SCOPE)
    assert "#ff0000" in values(result["colors"])
    # `html`, `body`, `#outside` and the six of the cards: `#gone` has no box.
    assert result["elements"] == 9


async def test_a_scope_reaches_into_an_open_shadow_tree(client: Client) -> None:
    result = await extract(client, SCOPE, scope="#deep")
    assert rows(result["colors"], "value", "uses") == [("#00ffff", 1)]
    assert result["elements"] == 1


async def test_a_family_with_no_value_in_the_scope_is_empty(client: Client) -> None:
    # The whole page holds the text, the radius and the shadow of `#outside`.
    page = await extract(client, SCOPE)
    typography = page["typography"]
    assert rows(typography["families"], "value", "uses") == [("Arial, sans-serif", 1)]
    assert rows(typography["sizes"], "value", "uses") == [(12, 1)]
    assert rows(typography["weights"], "value", "uses") == [(400, 1)]
    assert rows(typography["lineHeights"], "value", "uses") == [(16, 1)]
    assert rows(page["radii"], "value", "uses") == [("6px", 1)]
    assert rows(page["shadows"], "kind", "value", "uses") == [
        ("box", "rgba(0, 0, 0, 0.5) 0px 2px 4px 0px", 1)
    ]
    result = await extract(client, SCOPE, scope="#one-child")
    for family in families(result)[1:]:
        assert family == {"total": 0, "tokens": []}


async def test_a_scope_that_matches_no_element_fails(client: Client) -> None:
    message = await fail(client, SCOPE, scope=".missing")
    assert message == 'Scope ".missing" matched no elements.'


async def test_a_scope_that_is_not_a_selector_fails(client: Client) -> None:
    assert await fail(client, SCOPE, scope="div[") == 'Invalid selector "div[".'


async def test_a_scope_that_matches_only_elements_not_read_is_empty(
    client: Client,
) -> None:
    # `#gone` matches, and has no box.
    result = await extract(client, SCOPE, scope="#gone")
    assert result["elements"] == 0
    for family in families(result):
        assert family == {"total": 0, "tokens": []}


async def test_the_summary_of_an_empty_reading_counts_zeros(client: Client) -> None:
    result = await call(client, SCOPE, scope="#gone")
    assert result.is_error is False, texts(result)
    assert texts(result) == [
        "Tokens: colors 0, font families 0, font sizes 0, font weights 0, "
        "line heights 0, spacing 0, radii 0, shadows 0; elements 0; stabilized."
    ]


async def test_an_empty_scope_fails_and_is_not_the_whole_page(client: Client) -> None:
    message = await fail(client, SCOPE, scope="")
    assert not message.startswith("Tokens:")


async def test_an_element_that_paints_no_box_is_not_read_alone(
    client: Client,
) -> None:
    for scope in ("#none", "#flat-w", "#flat-h"):
        assert (await extract(client, USED, scope=scope))["elements"] == 0, scope


async def test_the_limit_keeps_the_most_used_tokens_in_family_order(
    client: Client,
) -> None:
    spacing = (await extract(client, LIMIT))["spacing"]
    # 210px has 2 Uses and comes first in Rank order; of the twenty of 1 Use,
    # 200px comes last by value and is cut.
    assert spacing["total"] == 21
    assert rows(spacing, "value") == [(value,) for value in TWENTY[:-1]] + [(210,)]


async def test_a_family_of_exactly_the_limit_is_whole(client: Client) -> None:
    spacing = (await extract(client, LIMIT, scope="#twenty"))["spacing"]
    assert spacing["total"] == 20
    assert rows(spacing, "value") == [(value,) for value in TWENTY]


async def test_the_limit_keeps_the_colors_that_come_first_by_text(
    client: Client,
) -> None:
    colors = (await extract(client, LIMIT))["colors"]
    # Twenty-one colours of 1 Use: `#ffffff` comes last by its text.
    assert colors["total"] == 21
    assert rows(colors, "value") == [
        ("#000000",),
        ("#000080",),
        ("#0000ff",),
        ("#008000",),
        ("#008080",),
        ("#0080ff",),
        ("#00ff00",),
        ("#00ffff",),
        ("#800000",),
        ("#800080",),
        ("#8000ff",),
        ("#808000",),
        ("#808080",),
        ("#80ff00",),
        ("#c0c0c0",),
        ("#ff0000",),
        ("#ff0080",),
        ("#ff00ff",),
        ("#ff8000",),
        ("#ffff00",),
    ]


async def test_the_summary_counts_every_token_found(client: Client) -> None:
    result = await call(client, LIMIT)
    assert result.is_error is False, texts(result)
    (text,) = texts(result)
    assert "colors 21," in text
    assert "spacing 21," in text


async def test_the_viewport_is_the_one_the_page_is_laid_out_in(
    client: Client,
) -> None:
    mobile = {"width": 375, "height": 812}
    result = await extract(client, VIEWPORT, viewport=mobile)
    # `#box` is `#111111` under `@media (max-width: 600px)` only.
    assert "#111111" in values(result["colors"])
    assert "#999999" not in values(result["colors"])
    assert result["viewport"] == mobile


async def test_an_unsupported_url_scheme_fails(client: Client) -> None:
    assert await fail(client, "ftp://example.com/") == (
        'Unsupported URL scheme "ftp"; use http://, https:// or file://.'
    )


async def test_a_page_that_cannot_be_loaded_fails(client: Client) -> None:
    url = (FIXTURES / "no-such-page.html").as_uri()
    assert (await fail(client, url)).startswith(f"Could not load {url}")


async def test_a_call_that_outlives_the_total_timeout_fails_and_the_next_succeeds(
    client: Client, local_server: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The only reach past the MCP boundary: 30 real seconds would slow every run.
    with monkeypatch.context() as patch, anyio.fail_after(10):
        patch.setattr(config, "TOTAL_TIMEOUT_S", 1.0)
        started = time.monotonic()
        message = await fail(client, f"{local_server}/hang")
        elapsed = time.monotonic() - started
    assert message == "Timed out after 1s."
    assert 1 <= elapsed < 2
    assert (await extract(client, PAGE))["elements"] == 8


async def test_a_page_that_never_goes_network_idle_is_read_unstabilized(
    client: Client, local_server: str
) -> None:
    result = await call(client, f"{local_server}/polling.html")
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    assert result.structured_content["stabilized"] is False
    (text,) = texts(result)
    assert text.endswith("; not stabilized.")


NO_STYLE_NOTICE = (
    " The page has no style of its own: these values are the browser's defaults."
)


def author(local_server: str, case: str = "") -> str:
    """The url of `tokens-author.html` with one style-like thing, or none."""
    return f"{local_server}/tokens-author.html{f'?{case}' if case else ''}"


async def test_author_styles_is_in_the_output_schema(client: Client) -> None:
    schema = (await tokens_tool(client)).output_schema
    assert schema is not None
    assert schema["properties"]["authorStyles"]["type"] == "boolean"
    assert "authorStyles" in schema["required"]


async def test_a_page_with_no_style_says_its_values_are_the_defaults(
    client: Client, local_server: str
) -> None:
    result = await call(client, author(local_server))
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    assert result.structured_content["authorStyles"] is False
    (text,) = texts(result)
    assert text.endswith(NO_STYLE_NOTICE), text


async def test_a_style_element_is_an_author_style(
    client: Client, local_server: str
) -> None:
    result = await call(client, author(local_server, "style"))
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    assert result.structured_content["authorStyles"] is True
    (text,) = texts(result)
    assert "no style of its own" not in text


@pytest.mark.parametrize(
    "case",
    [
        "link",
        "attribute",
        "adopted",
        "shadow-style",
        "shadow-adopted",
        "cross-origin",
        "print",
    ],
)
async def test_each_author_style_turns_the_notice_off(
    client: Client, local_server: str, case: str
) -> None:
    result = await extract(client, author(local_server, case))
    assert result["authorStyles"] is True


@pytest.mark.parametrize(
    "case", ["empty-style", "empty-attribute", "missing-link", "disabled", "bgcolor"]
)
async def test_what_is_no_author_style_leaves_the_notice_on(
    client: Client, local_server: str, case: str
) -> None:
    result = await extract(client, author(local_server, case))
    assert result["authorStyles"] is False


async def test_author_styles_describes_the_whole_page_whatever_the_scope(
    client: Client, local_server: str
) -> None:
    result = await extract(client, author(local_server, "style"), scope="#inside")
    assert result["elements"] == 1
    assert result["authorStyles"] is True


async def test_the_other_tools_gain_no_field(client: Client, local_server: str) -> None:
    url = author(local_server)
    inspected = await client.call_tool(
        "inspect_element", {"url": url, "selector": "#inside"}
    )
    assert inspected.structured_content is not None, texts(inspected)
    assert set(inspected.structured_content) == {
        "box",
        "boxModel",
        "computed",
        "sampledColors",
        "stabilized",
        "viewport",
    }
    detected = await client.call_tool("detect_visual_bugs", {"url": url})
    assert detected.structured_content is not None, texts(detected)
    assert set(detected.structured_content) == {"findings", "captures"}
    for captured in detected.structured_content["captures"]:
        assert set(captured) == {"viewport", "stabilized"}


async def test_the_description_tells_author_styles(client: Client) -> None:
    description = " ".join(((await tokens_tool(client)).description or "").split())
    assert "`authorStyles`" in description
    assert "the whole page, whatever `scope` is" in description
    assert "the browser's defaults" in description
