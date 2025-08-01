from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers import map_to
from guilt.types.json import Json
from guilt.utility import guilt_user_file_paths
from typing import cast
import json

class CpuProfilesConfigService(CpuProfilesConfigServiceInterface):
  def __init__(
    self,
    user_service: UserServiceInterface
  ) -> None:
    self.user_service = user_service
    
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
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot read CPU profiles config.")

    with guilt_user_file_paths.get_cpu_profiles_config_path(current_user).open('r') as file:
      return map_to.cpu_profiles_config.from_json(
        cast(Json, json.load(file))
      )

  def write_to_file(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot write CPU profiles config.")

    path = guilt_user_file_paths.get_cpu_profiles_config_path(current_user)
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_cpu_profiles_config(cpu_profiles_config),
        file,
        indent=2
      )