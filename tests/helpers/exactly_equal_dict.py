from typing import Any

def exactly_equal_dict(a: dict[str, Any], b: dict[str, Any]) -> bool:
  return all(
    key in b and type(a[key]) == type(b[key]) and a[key] == b[key]
    for key in a
  )