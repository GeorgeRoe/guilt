import pytest
from typing import Callable, Any, Type, get_type_hints, get_args, cast, get_origin
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json

def get_base_type(given_type: Type[Any]) -> Type[Any]:
  return get_origin(given_type) or given_type

type_instances: list[Json] = [
  None,
  True,
  1,
  0.99,
  "Hello, World!",
  [],
  {}
]

type_instance_map: dict[Type[Any], Json] = {get_base_type(type(item)): item for item in type_instances}

expect_methods: list[Callable[[Json], Json]] = [
  JsonReader.expect_bool,
  JsonReader.expect_int,
  JsonReader.expect_float,
  JsonReader.expect_str,
  JsonReader.expect_list,
  JsonReader.expect_dict
]

type_method_map: dict[Type[Any], Callable[[Json], Json]] = {get_base_type(get_type_hints(method)['return']): method for method in expect_methods}

json_base_types = [get_base_type(item) for item in cast(tuple[Type[Json]], get_args(Json))]

@pytest.mark.parametrize(
  "method, value, expected",
  [
    (method, value, value)
    for method, value
    in {
      method: type_instance_map.get(return_type)
      for return_type, method
      in type_method_map.items()
    }.items()
  ]
)
def test_expect_type_valid(method: Callable[[Any], Any], value: Any, expected: Any):
  assert method(value) == expected
  
@pytest.mark.parametrize(
  "method, value",
  [
    (method, value)
    for expected_type, method in type_method_map.items()
    for actual_type, value in type_instance_map.items()
    if actual_type != expected_type
  ]
)
def test_expect_type_invalid(method: Callable[[Any], Any], value: Any):
  with pytest.raises(ValueError):
    method(value)