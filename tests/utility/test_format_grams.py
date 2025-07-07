import pytest
from typing import Union
from guilt.utility.format_grams import format_grams

@pytest.mark.parametrize(
    "grams, expected",
    [
        (0.1234, "0.12 grams"),
        (0.999, "1.00 grams"),
        (1, "1 gram"),
        (2, "2 grams"),
        (999, "999 grams"),
        (1000, "1.00 kilogram"),
        (1500, "1.50 kilograms"),
        (999999, "999.99 kilograms"),
        (1_000_000, "1.00 tonne"),
        (2_500_000, "2.50 tonnes"),
    ]
)
def test_format_grams(grams: Union[int, float], expected: str):
    assert format_grams(grams) == expected