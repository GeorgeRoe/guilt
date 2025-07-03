from dataclasses import dataclass

@dataclass
class CpuProfile:
  name: str
  tdp: float
  cores: int
  
  @property
  def tdp_per_core(self) -> float:
    return self.tdp / self.cores if self.cores else 0