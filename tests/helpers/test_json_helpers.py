from guilt.types.json import Json
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_given_key_incorrectly_typed, all_variants_with_one_key_incorrectly_typed, json_instances
from tests.helpers.exactly_equal_dict import exactly_equal_dict

def test_all_variants_with_one_key_removed() -> None:
  data: dict[str, Json] = {
    "a": 1,
    "b": 2,
    "c": 3
  }
  
  result = all_variants_with_one_key_removed(data)
  
  assert result == [
    {
      "b": 2,
      "c": 3
    },
    {
      "a": 1,
      "c": 3
    },
    {
      "a": 1,
      "b": 2
    }
  ]
  
def test_all_variants_with_given_key_incorrectly_typed() -> None:
  data: dict[str, Json] = {
    "key": "value"
  }
  
  result = all_variants_with_given_key_incorrectly_typed(data, "key", False)
  
  assert result == [
    { "key": None },
    { "key": True },
    { "key": 1 },
    { "key": 0.99 },
    { "key": [] },
    { "key": {} }
  ]
  
def test_all_variants_with_given_key_incorrectly_typed_number() -> None:
  data: dict[str, Json] = {
    "key": 1,
  }
  
  result = all_variants_with_given_key_incorrectly_typed(data, "key", True)
  
  print(result)
  
  assert result == [
    { "key": None },
    { "key": True },
    { "key": "Hello, World!" },
    { "key": [] },
    { "key": {} }
  ]
  
def test_all_variants_with_one_key_incorrectly_typed() -> None:
  data: dict[str, Json] = {
    "dict": {},
    "list": []
  }
  
  result = all_variants_with_one_key_incorrectly_typed(data)
  
  assert not data in result
  assert len(result) == 2 * (len(json_instances) - 1)
  
def test_all_variants_with_one_key_incorrectly_typed_number() -> None:
  data: dict[str, Json] = {
    "int": int(1),
    "float": float(1),
    "list": []
  }
  
  result = all_variants_with_one_key_incorrectly_typed(data, {"int", "float"})

  assert len(result) == 2 * (len(json_instances) - 2) + (len(json_instances) - 1)
  assert all(not exactly_equal_dict(item, data) for item in result)