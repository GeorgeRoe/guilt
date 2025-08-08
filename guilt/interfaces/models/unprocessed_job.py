from abc import ABC, abstractmethod
from guilt.interfaces.models.cpu_profile import CpuProfileInterface

class UnprocessedJobInterface(ABC):
  @property
  @abstractmethod
  def job_id(self) -> str:
    pass

  @property
  @abstractmethod
  def cpu_profile(self) -> CpuProfileInterface:
    pass