from abc import ABC, abstractmethod
from guilt.models.cpu_profiles_config import CpuProfilesConfig

class CpuProfilesConfigServiceInterface(ABC):
  @abstractmethod
  def get_default(self) -> CpuProfilesConfig:
    pass
  
  @abstractmethod
  def read_from_file(self) -> CpuProfilesConfig:
    pass
  
  @abstractmethod
  def write_to_file(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    pass