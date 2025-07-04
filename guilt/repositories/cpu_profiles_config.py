from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers import map_to
from guilt.constants.paths import CPU_PROFILES_PATH
import json

class CpuProfilesConfigRepository:  
  def get_default_data(self) -> CpuProfilesConfig:
    default = CpuProfile("AMD EPYC 9654", 360, 96)
    
    profiles = [
      default,
      CpuProfile("AMD EPYC 7502", 180, 32),
      CpuProfile("AMD EPYC 7742", 225, 64),
      CpuProfile("AMD EPYC 7543P", 225, 32)
    ]
    
    return CpuProfilesConfig(default, {profile.name: profile for profile in profiles})
  
  def fetch_data(self) -> CpuProfilesConfig:
    with CPU_PROFILES_PATH.open("r") as file:
      return map_to.cpu_profiles_config.from_json_file_contents(json.load(file))
  
  def submit_data(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    CPU_PROFILES_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with CPU_PROFILES_PATH.open("w") as file:
      json.dump(map_to.json_file_contents.from_cpu_profiles_config(cpu_profiles_config), file, indent=2)