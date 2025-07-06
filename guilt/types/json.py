from typing import Union

Json = Union[
  None,
  bool,
  int,
  float,
  str,
  list["Json"],
  dict[str, "Json"]
]