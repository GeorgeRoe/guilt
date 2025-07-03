from guilt.models.cpu_profile import CpuProfile
from guilt.utility.safe_get import safe_get_string, safe_get_float, safe_get_int
from typing import Any

class MapToCpuProfile:
  @staticmethod
  def from_json_file_contents(data: dict[str, Any]) -> CpuProfile:
    name = safe_get_string(data, "name")
    tdp = safe_get_float(data, "tdp")
    cores = safe_get_int(data, "cores")
    return CpuProfile(name, tdp, cores)