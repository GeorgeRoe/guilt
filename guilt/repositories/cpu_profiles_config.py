from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json_file_contents import MapToJsonFileContents
from guilt.mappers.cpu_profiles_config import MapToCpuProfilesConfig
from pathlib import Path
from typing import Final
import json

class CpuProfilesConfigRepository:
  DEFAULT_PATH: Final[Path] = Path.home() / ".guilt" / "cpu_profiles.json"
  
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
    with self.DEFAULT_PATH.open("r") as file:
      return MapToCpuProfilesConfig.from_json_file_contents(json.load(file))
  
  def submit_data(self, cpu_profiles_config: CpuProfilesConfig) -> None:
    self.DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with self.DEFAULT_PATH.open("w") as file:
      json.dump(MapToJsonFileContents.from_cpu_profiles_config(cpu_profiles_config), file, indent=2)