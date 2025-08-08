from guilt.models.guilt_script_directives import GuiltScriptDirectives
from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.types.json import Json
from guilt.utility import json_reader

class MapToGuiltScriptDirectives:
  @staticmethod
  def from_json_directives(directives: dict[str, Json], cpu_profiles_repository: CpuProfilesRepositoryInterface) -> GuiltScriptDirectives:
    cpu_profile_name = json_reader.ensure_get_str(directives, "cpu-profile")
    cpu_profile = cpu_profiles_repository.get(cpu_profile_name)

    if cpu_profile is None:
      raise Exception(f"Couldnt find given cpu profile '{cpu_profile_name}'")
    
    return GuiltScriptDirectives(
      cpu_profile=cpu_profile
    )