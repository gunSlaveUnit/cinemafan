import pytest

from movies.utils import form_periods_movie_showing


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
def test_form_periods_movie_showing(value: list[int], result: str):
    assert form_periods_movie_showing(value) == result
