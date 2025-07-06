from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from guilt.mappers.cpu_profile import MapToCpuProfile

class MapToCpuProfilesConfig:
  @staticmethod
  def from_json(data: Json) -> CpuProfilesConfig:
    data = JsonReader.expect_dict(data)
    
    profiles: list[CpuProfile] = []
    profiles_data = JsonReader.ensure_get_dict(data, "profiles")
    for name, profile_values in profiles_data.items():
      profile_data = JsonReader.expect_dict(profile_values)
      profile_data["name"] = name
      profiles.append(MapToCpuProfile.from_json(profile_data))
    
    profile_map = {profile.name: profile for profile in profiles}
    
    default_profile = profile_map.get(JsonReader.ensure_get_str(data, "default"))
    if default_profile is None:
      raise ValueError("The given default cpu name does not correspond to an existing cpu profile")
    
    return CpuProfilesConfig(default_profile, profile_map)