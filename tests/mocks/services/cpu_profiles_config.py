from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.models.cpu_profiles_config import CpuProfilesConfig
import copy

class MockCpuProfilesConfigService(CpuProfilesConfigServiceInterface):
  def __init__(self, default: CpuProfilesConfig, fail: bool = False) -> None:
    self._default = default
    self._file = copy.deepcopy(self._default)
    self._fail = fail
    
  def get_default(self) -> CpuProfilesConfig:
    return copy.deepcopy(self._default)
  
  def read_from_file(self) -> CpuProfilesConfig:
    if self._fail: raise Exception("Failed to read from file")
    return self._file
  
  def write_to_file(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    if self._fail: raise Exception("Failed to write to file")
    self._file = cpu_profiles_config