import pytest
from guilt.mappers.get_entries_password_result import MapToGetEntriesPasswordResult
from guilt.models.get_entires_password_result import GetEntriesPasswordResult
from pathlib import Path

VALID_LINE = "username:password:user_id:primary_group_id:info:/path/to/home:/path/to/shell"

def test_from_line_success() -> None:
  result = MapToGetEntriesPasswordResult.from_line(VALID_LINE)

  assert isinstance(result, GetEntriesPasswordResult)

  assert result.username == "username"
  assert result.password == "password"
  assert result.user_id == "user_id"
  assert result.primary_group_id == "primary_group_id"
  assert result.info == "info"
  assert result.home_directory == Path("/path/to/home")
  assert result.shell == Path("/path/to/shell")

@pytest.mark.parametrize(
  "line",
  [
    "",
    VALID_LINE + ":extra_field"
  ]
)
def test_from_line_invalid_raises(line: str) -> None:
  with pytest.raises(ValueError):
    MapToGetEntriesPasswordResult.from_line(line)