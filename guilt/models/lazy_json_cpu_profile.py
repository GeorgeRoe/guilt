from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from guilt.utility import json_reader
from guilt.types.json import Json
from typing import Optional

class LazyJsonCpuProfile(CpuProfileInterface):
  def __init__(self, data: Json) -> None:
    self._data = json_reader.expect_dict(data)

    self._name: Optional[str] = None
    self._tdp: Optional[float] = None
    self._cores: Optional[int] = None

  @property
  def name(self) -> str:
    if self._name is None:
      self._name = json_reader.ensure_get_str(self._data, "name")
    return self._name
  
  @property
  def tdp(self) -> float:
    if self._tdp is None:
      self._tdp = float(json_reader.ensure_get_number(self._data, "tdp"))
    return self._tdp
  
  @property
  def cores(self) -> int:
    if self._cores is None:
      self._cores = int(json_reader.ensure_get_number(self._data, "cores"))
    return self._cores