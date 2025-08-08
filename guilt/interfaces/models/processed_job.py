from abc import ABC, abstractmethod
from datetime import datetime
from guilt.interfaces.models.cpu_profile import CpuProfileInterface

class ProcessedJobInterface(ABC):
  @property
  @abstractmethod
  def start(self) -> datetime:
    pass

  @property
  @abstractmethod
  def end(self) -> datetime:
    pass

  @property
  @abstractmethod
  def job_id(self) -> str:
    pass

  @property
  @abstractmethod
  def cpu_profile(self) -> CpuProfileInterface:
    pass

  @property
  @abstractmethod
  def energy(self) -> float:
    pass

  @property
  @abstractmethod
  def emissions(self) -> float:
    pass

  @property
  @abstractmethod
  def generation_mix(self) -> dict[str, float]:
    pass