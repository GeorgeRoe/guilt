from datetime import datetime
from typing import Any, cast

def ensure_get_value(data: dict[str, Any], key: str) -> Any:
  value = data.get(key)
  
  if value is None:
    raise ValueError(f"The key '{key}' is required.")
  
  return value

def safe_get_dict(data: dict[str, Any], key: str) -> dict[str, Any]:
  value = ensure_get_value(data, key)
  
  if not isinstance(value, dict):
    raise ValueError(f"The value for key '{key}' should be a dict.")
  
  return cast(dict[str, Any], value)

def safe_get_list(data: dict[str, Any], key: str) -> list[Any]:
  value = ensure_get_value(data, key)
  
  if not isinstance(value, list):
    raise ValueError(f"The value for key '{key}' should be a list.")
  
  return cast(list[Any], value)
  
def safe_get_string(data: dict[str, Any], key: str) -> str:  
  return str(ensure_get_value(data, key))

def safe_get_float(data: dict[str, Any], key: str) -> float:
  return float(safe_get_string(data, key))

def safe_get_int(data: dict[str, Any], key: str) -> int:
  return int(safe_get_string(data, key))