"""The CIEDE2000 colour difference, the one test below the MCP tool boundary."""

from pathlib import Path

from squint_mcp.color import delta_e_2000

# The test data of Sharma, Wu and Dalal (2005), as published: on each row two
# Lab colours (L, a, b of each) and their ΔE2000.
DATA = Path(__file__).parent / "fixtures" / "ciede2000testdata.txt"


def test_delta_e_2000_gives_the_published_value_of_each_of_the_34_pairs() -> None:
    rows = [
        [float(number) for number in line.split()]
        for line in DATA.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    assert len(rows) == 34
    for l1, a1, b1, l2, a2, b2, published in rows:
        first, second = (l1, a1, b1), (l2, a2, b2)
        assert round(delta_e_2000(first, second), 4) == published
        assert round(delta_e_2000(second, first), 4) == published
