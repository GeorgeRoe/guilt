from guilt.models.cpu_profile import CpuProfile
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader

class MapToCpuProfile:
  @staticmethod
  def from_json(data: Json) -> CpuProfile:
    data = JsonReader.expect_dict(data)
    name = JsonReader.ensure_get_str(data, "name")
    tdp = float(JsonReader.ensure_get_number(data, "tdp"))
    cores = int(JsonReader.ensure_get_number(data, "cores"))
    return CpuProfile(name, tdp, cores)