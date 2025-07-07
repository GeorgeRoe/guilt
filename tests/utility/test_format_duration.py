import pytest
from guilt.utility.format_duration import format_duration

@pytest.mark.parametrize(
    "seconds, expected",
    [
        (0, "0 seconds"),
        (59, "59 seconds"),
        (60, "1 minute"),
        (61, "1 minute, 1 second"),
        (3600, "1 hour"),
        (3661, "1 hour, 1 minute, 1 second"),
        (86400, "1 day"),
        (90061, "1 day, 1 hour, 1 minute, 1 second"),
        (172800, "2 days"),
    ]
)
def test_format_duration(seconds: float, expected: str) -> None:
    assert format_duration(seconds) == expected