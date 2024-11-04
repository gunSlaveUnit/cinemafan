import pytest

from .routes import format_years


@pytest.mark.parametrize(
    "value, result",
    [
        ([2000], "2000"),
        ([2000, 2001], "2000 - 2001"),
        ([2000, 2002], "2000, 2002"),
        ([2000, 2001, 2002], "2000 - 2002"),
        ([2000, 2001, 2003, 2004], "2000 - 2001, 2003 - 2004"),
        ([2000, 2002, 2004, 2006], "2000, 2002, 2004, 2006"),
    ]
)
def test_format_years(value: list[int], result: str):
    assert format_years(value) == result
