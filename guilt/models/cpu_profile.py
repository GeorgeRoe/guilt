from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from dataclasses import dataclass

@dataclass
class CpuProfile(CpuProfileInterface):
  name: str
  tdp: float
  cores: int