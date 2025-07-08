import pytest
from typing import Callable, Any, Type, get_type_hints, get_args, cast
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json
from tests.helpers.get_base_type import get_base_type
from tests.helpers.json_helpers import json_base_type_instance_map

expect_methods: list[Callable[[Json], Json]] = [
  JsonReader.expect_bool,
  JsonReader.expect_int,
  JsonReader.expect_float,
  JsonReader.expect_str,
  JsonReader.expect_list,
  JsonReader.expect_dict
]

type_expect_method_map: dict[Type[Any], Callable[[Json], Json]] = {get_base_type(get_type_hints(method)['return']): method for method in expect_methods}

ensure_methods: list[Callable[[dict[str, Json], str], Json]] = [
  JsonReader.ensure_get_bool,
  JsonReader.ensure_get_int,
  JsonReader.ensure_get_float,
  JsonReader.ensure_get_str,
  JsonReader.ensure_get_list,
  JsonReader.ensure_get_dict
]

type_ensure_method_map: dict[Type[Any], Callable[[dict[str, Json], str], Json]] = {
  get_base_type(get_type_hints(method)['return']): method for method in ensure_methods
}

json_base_types = [get_base_type(item) for item in cast(tuple[Type[Json]], get_args(Json))]

@pytest.mark.parametrize(
  "method, value",
  [
    (method, json_base_type_instance_map.get(return_type))
    for return_type, method
    in type_expect_method_map.items()
  ] + [
    (JsonReader.expect_number, 1),
    (JsonReader.expect_number, 0.99)
  ]
)
def test_expect_type_valid(method: Callable[[Any], Any], value: Any):
  assert method(value) == value
  
@pytest.mark.parametrize(
  "method, value",
  [
    (method, value)
    for expected_type, method in type_expect_method_map.items()
    for actual_type, value in json_base_type_instance_map.items()
    if actual_type != expected_type
  ] + [
    (JsonReader.expect_number, value)
    for actual_type, value in json_base_type_instance_map.items()
    if not actual_type in {int, float}
  ]
)
def test_expect_type_invalid(method: Callable[[Any], Any], value: Any):
  with pytest.raises(ValueError):
    method(value)
    
@pytest.mark.parametrize(
  "method, key, value",
  [
    (method, "x", value)
    for return_type, method in type_ensure_method_map.items()
    for actual_type, value in json_base_type_instance_map.items()
    if actual_type == return_type
  ] + [
    (JsonReader.ensure_get_number, "x", 1),
    (JsonReader.ensure_get_number, "x", 0.99)
  ]
)
def test_ensure_get_valid(method: Callable[[dict[str, Json], str], Json], key: str, value: Json):
  data = {key: value}
  assert method(data, key) == value  

@pytest.mark.parametrize(
  "method",
  list(type_ensure_method_map.values())
)
def test_ensure_get_missing_key(method: Callable[[dict[str, Json], str], Json]):
  with pytest.raises(ValueError):
    method({}, "missing")
    
@pytest.mark.parametrize(
  "method, wrong_value",
  [
    (method, value)
    for expected_type, method in type_ensure_method_map.items()
    for actual_type, value in json_base_type_instance_map.items()
    if actual_type != expected_type
  ] + [
    (JsonReader.ensure_get_number, value)
    for actual_type, value in json_base_type_instance_map.items()
    if not actual_type in {int, float}
  ]
)
def test_ensure_get_invalid_type(method: Callable[[dict[str, Json], str], Json], wrong_value: Json):
  with pytest.raises(ValueError):
    method({"x": wrong_value}, "x")