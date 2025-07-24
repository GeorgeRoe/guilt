from guilt.models.slurm_script_directives import SlurmScriptDirectives
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from guilt.utility.parse_timedelta_string import parse_timedelta_string

class MapToSlurmScriptDirectives:
  @staticmethod
  def from_json_directives(directives: dict[str, Json]) -> SlurmScriptDirectives:
    return SlurmScriptDirectives(
      time=parse_timedelta_string(JsonReader.ensure_get_str(directives, "time"))
    )