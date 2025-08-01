from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers import map_to
from guilt.types.json import Json
from typing import cast
import json

class CpuProfilesConfigService(CpuProfilesConfigServiceInterface):
  def __init__(
    self,
    guilt_directory_service: GuiltDirectoryServiceInterface
  ) -> None:
    self.guilt_directory_service = guilt_directory_service
    
  def get_default(self) -> CpuProfilesConfig:
    default_profile = CpuProfile("AMD EPYC 9654", 360, 96)
    
    profiles = [
      default_profile,
      CpuProfile("AMD EPYC 7502", 180, 32),
      CpuProfile("AMD EPYC 7742", 225, 64),
      CpuProfile("AMD EPYC 7543P", 225, 32)
    ]
    
    return CpuProfilesConfig(default_profile, {profile.name: profile for profile in profiles})
  
  def read_from_file(self) -> CpuProfilesConfig:
    with self.guilt_directory_service.get_cpu_profiles_config_path().open('r') as file:
      return map_to.cpu_profiles_config.from_json(
        cast(Json, json.load(file))
      )

  def write_to_file(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    path = self.guilt_directory_service.get_cpu_profiles_config_path()
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_cpu_profiles_config(cpu_profiles_config),
        file,
        indent=2
      )