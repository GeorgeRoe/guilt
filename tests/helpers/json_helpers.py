from guilt.types.json import Json
from tests.helpers.get_base_type import get_base_type
from typing import Type, Any
from itertools import chain

json_instances: list[Json] = [
  None,
  True,
  1,
  0.99,
  "Hello, World!",
  [],
  {}
]

json_type_instance_map: dict[Type[Json], Json] = {
  type(value): value
  for value
  in json_instances
}

json_base_type_instance_map: dict[Type[Any], Json] = {
  get_base_type(json_subtype): value
  for json_subtype, value
  in json_type_instance_map.items()
}

def all_variants_with_one_key_removed(data: dict[str, Json]) -> list[dict[str, Json]]:
  return [
    {
      key: value 
      for key, value
      in data.items()
      if key != key_to_remove
    }
    for key_to_remove
    in data
  ]
  
def all_variants_with_given_key_incorrectly_typed(data: dict[str, Json], modify_key: str, is_number: bool) -> list[dict[str, Json]]:
  original_type: Type[Any] = get_base_type(type(data.get(modify_key)))
  
  return [
    {
      **data,
      modify_key: instance
    }
    for base_type, instance
    in json_base_type_instance_map.items()
    if (
      base_type != original_type if not is_number
      else not base_type in {int, float} or base_type is bool
    )
  ]
  
def all_variants_with_one_key_incorrectly_typed(data: dict[str, Json], number_keys: set[str] = set(), ignore_keys: set[str] = set()) -> list[dict[str, Json]]:
  return list(chain.from_iterable(
    all_variants_with_given_key_incorrectly_typed(data, key, key in number_keys)
    for key in data
    if not key in ignore_keys
  ))