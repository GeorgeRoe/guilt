from abc import ABC, abstractmethod
from typing import Optional
from guilt.interfaces.models.cpu_profile import CpuProfileInterface

class SettingsRepositoryInterface(ABC):
  @abstractmethod
  def get_default_cpu_profile(self) -> Optional[CpuProfileInterface]:
    pass

  @abstractmethod
  def set_default_cpu_profile(self, cpu_profile: CpuProfileInterface) -> bool:
    pass

  @abstractmethod
  def save(self) -> bool:
    pass