from guilt.models.cpu_profiles_config import CpuProfilesConfig
from typing import Any
from dataclasses import asdict

class MapToJsonFileContents:
  @staticmethod
  def from_cpu_profiles_config(cpu_profiles_config: CpuProfilesConfig) -> dict[str, Any]:   
    return {
      "default": cpu_profiles_config.default.name,
      "profiles": {
        profile.name: {key: value for key, value in asdict(profile).items() if key != "name"}
        for profile in cpu_profiles_config.profiles.values()
      }
    }