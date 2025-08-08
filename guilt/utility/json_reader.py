from guilt.types.json import Json
from typing import Type, TypeVar, cast, Union, get_origin

T = TypeVar("T")

def _expect_type(data: Json, expected_type: Type[T]) -> T:
  base_expected_type = get_origin(expected_type) or expected_type
  
  if base_expected_type in {int, float} and isinstance(data, bool):
    raise ValueError(f"Expected {base_expected_type.__name__}, got bool")
  
  if isinstance(data, base_expected_type):
    return cast(T, data)
  raise ValueError(f"Expected JSON data to be of type '{expected_type.__name__}', but got '{type(data).__name__}'") 

def expect_bool(data: Json) -> bool:
  return _expect_type(data, bool)

def expect_int(data: Json) -> int:
  return _expect_type(data, int)

def expect_float(data: Json) -> float:
  return _expect_type(data, float)

def expect_str(data: Json) -> str:
  return _expect_type(data, str)
  
def expect_list(data: Json) -> list[Json]:
  return _expect_type(data, list[Json])

def expect_dict(data: Json) -> dict[str, Json]:
  return _expect_type(data, dict[str, Json])

def expect_number(data: Json) -> Union[int, float]:
  if isinstance(data, (int, float)) and not isinstance(data, bool):
    return data
  raise ValueError(f"Expected number (int or float), but got {type(data).__name__}")

def ensure_get_json(data: dict[str, Json], key: str) -> Json:
  value = data.get(key)
  
  if value is None:
    raise ValueError(f"The key '{key}' is required.")
  
  return value

def _ensure_get_type(data: dict[str, Json], key: str, expected_type: Type[T]) -> T:
  return _expect_type(ensure_get_json(data, key), expected_type)

def ensure_get_bool(data: dict[str, Json], key: str) -> bool:
  return _ensure_get_type(data, key, bool)

def ensure_get_int(data: dict[str, Json], key: str) -> int:
  return _ensure_get_type(data, key, int)

def ensure_get_float(data: dict[str, Json], key: str) -> float:
  return _ensure_get_type(data, key, float)

def ensure_get_str(data: dict[str, Json], key: str) -> str:
  return _ensure_get_type(data, key, str)
  
def ensure_get_list(data: dict[str, Json], key: str) -> list[Json]:
  return _ensure_get_type(data, key, list[Json])

def ensure_get_dict(data: dict[str, Json], key: str) -> dict[str, Json]:
  return _ensure_get_type(data, key, dict[str, Json])

def ensure_get_number(data: dict[str, Json], key: str) -> Union[int, float]:
  return expect_number(ensure_get_json(data, key))