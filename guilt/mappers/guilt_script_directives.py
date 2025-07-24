from guilt.models.guilt_script_directives import GuiltScriptDirectives
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from guilt.models.cpu_profiles_config import CpuProfilesConfig

class MapToGuiltScriptDirectives:
  @staticmethod
  def from_json_directives(directives: dict[str, Json], cpu_profiles_config: CpuProfilesConfig) -> GuiltScriptDirectives:
    cpu_profile_name = JsonReader.ensure_get_str(directives, "cpu-profile")
    cpu_profile = cpu_profiles_config.profiles.get(cpu_profile_name)
    
    if cpu_profile is None:
      raise Exception(f"Couldnt find given cpu profile '{cpu_profile_name}'")
    
    return GuiltScriptDirectives(
      cpu_profile=cpu_profile
    )