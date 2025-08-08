from guilt.interfaces.models.cpu_profile import CpuProfileInterface

class CpuProfile(CpuProfileInterface):
  def __init__(self, name: str, tdp: float, cores: int) -> None:
    self._name = name
    self._tdp = tdp
    self._cores = cores

  @property
  def name(self) -> str:
    return self._name
  
  @property
  def tdp(self) -> float:
    return self._tdp
  
  @property
  def cores(self) -> int:
    return self._cores