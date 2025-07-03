from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.utility.safe_get import safe_get_dict, safe_get_float, safe_get_int, safe_get_string
from typing import Any

class MapToCpuProfilesConfig:
  @staticmethod
  def from_json_file_contents(data: dict[str, Any]) -> CpuProfilesConfig:
    profiles: list[CpuProfile] = []
    
    profiles_data = safe_get_dict(data, "profiles")
    for name, profile_data in profiles_data.items():
      profiles.append(CpuProfile(
        name,
        safe_get_float(profile_data, "tdp"),
        safe_get_int(profile_data, "cores")
      ))
      
    profile_map = {profile.name: profile for profile in profiles}
    
    default_profile = profile_map.get(safe_get_string(data, "default"))
    if default_profile is None:
      raise ValueError("The given default cpu name does not correspond to an existing cpu profile")
    
    return CpuProfilesConfig(default_profile, profile_map)
    
