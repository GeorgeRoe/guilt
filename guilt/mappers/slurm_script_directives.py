from guilt.models.slurm_script_directives import SlurmScriptDirectives
from guilt.types.json import Json
from guilt.utility import json_reader
from guilt.utility.parse_timedelta_string import parse_timedelta_string

class MapToSlurmScriptDirectives:
  @staticmethod
  def from_json_directives(directives: dict[str, Json]) -> SlurmScriptDirectives:
    return SlurmScriptDirectives(
      time=parse_timedelta_string(json_reader.ensure_get_str(directives, "time")),
      nodes=json_reader.ensure_get_int(directives, "nodes"),
      tasks_per_node=json_reader.ensure_get_int(directives, "tasks-per-node"),
      cpus_per_task=json_reader.ensure_get_int(directives, "cpus-per-task")
    )