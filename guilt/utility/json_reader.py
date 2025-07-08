from guilt.types.json import Json
from typing import Type, TypeVar, cast, Union, get_origin

T = TypeVar("T")

class JsonReader:
  @staticmethod
  def _expect_type(data: Json, expected_type: Type[T]) -> T:
    if isinstance(data, get_origin(expected_type) or expected_type):
      return cast(T, data)
    raise ValueError(f"Expected JSON data to be of type '{expected_type.__name__}', but got '{type(data).__name__}'") 

  @classmethod
  def expect_bool(cls, data: Json) -> bool:
    return cls._expect_type(data, bool)
  
  @classmethod
  def expect_int(cls, data: Json) -> int:
    if isinstance(data, bool):
      raise ValueError("Expected int, got bool")
    return cls._expect_type(data, int)
  
  @classmethod
  def expect_float(cls, data: Json) -> float:
    if isinstance(data, bool):
      raise ValueError("Expected float, got bool")
    return cls._expect_type(data, float)
  
  @classmethod
  def expect_str(cls, data: Json) -> str:
    return cls._expect_type(data, str)
    
  @classmethod
  def expect_list(cls, data: Json) -> list[Json]:
    return cls._expect_type(data, list[Json])
  
  @classmethod
  def expect_dict(cls, data: Json) -> dict[str, Json]:
    return cls._expect_type(data, dict[str, Json])
  
  @staticmethod
  def expect_number(data: Json) -> Union[int, float]:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
      return data
    raise ValueError(f"Expected number (int or float), but got {type(data).__name__}")
  
  @staticmethod
  def ensure_get_json(data: dict[str, Json], key: str) -> Json:
    value = data.get(key)
    
    if value is None:
      raise ValueError(f"The key '{key}' is required.")
    
    return value
  
  @classmethod
  def _ensure_get_type(cls, data: dict[str, Json], key: str, expected_type: Type[T]) -> T:
    return cls._expect_type(cls.ensure_get_json(data, key), expected_type)
  
  @classmethod
  def ensure_get_bool(cls, data: dict[str, Json], key: str) -> bool:
    return cls._ensure_get_type(data, key, bool)
  
  @classmethod
  def ensure_get_int(cls, data: dict[str, Json], key: str) -> int:
    return cls._ensure_get_type(data, key, int)
  
  @classmethod
  def ensure_get_float(cls, data: dict[str, Json], key: str) -> float:
    return cls._ensure_get_type(data, key, float)
  
  @classmethod
  def ensure_get_str(cls, data: dict[str, Json], key: str) -> str:
    return cls._ensure_get_type(data, key, str)
    
  @classmethod
  def ensure_get_list(cls, data: dict[str, Json], key: str) -> list[Json]:
    return cls._ensure_get_type(data, key, list[Json])
  
  @classmethod
  def ensure_get_dict(cls, data: dict[str, Json], key: str) -> dict[str, Json]:
    return cls._ensure_get_type(data, key, dict[str, Json])
  
  @classmethod
  def ensure_get_number(cls, data: dict[str, Json], key: str) -> Union[int, float]:
    return cls.expect_number(cls.ensure_get_json(data, key))