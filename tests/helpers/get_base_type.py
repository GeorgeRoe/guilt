from typing import Type, Any, get_origin

def get_base_type(given_type: Type[Any]) -> Type[Any]:
  return get_origin(given_type) or given_type