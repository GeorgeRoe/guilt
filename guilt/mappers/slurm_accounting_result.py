from typing import Any, cast
from datetime import datetime, timezone
from guilt.utility.safe_get import safe_get_string, safe_get_dict, safe_get_float, safe_get_list
from guilt.models.slurm_accounting_result import SlurmAccountingResult

class MapToSlurmAccountingResult:
  @staticmethod
  def from_command_dict(data: dict[str, Any]) -> SlurmAccountingResult:
    job_id = safe_get_string(data, "job_id")
        
    time = safe_get_dict(data, "time")

    start = datetime.fromtimestamp(safe_get_float(time, "start")).replace(tzinfo=timezone.utc)
    end = datetime.fromtimestamp(safe_get_float(time, "end")).replace(tzinfo=timezone.utc)
    
    resources = data.get("tres")
    if resources is None:
      raise ValueError("Tres is required.")
    
    resources = safe_get_dict(data, "tres")
    allocated = safe_get_list(resources, "allocated")
    
    allocated_resource_counts: dict[str, float] = {}
    for item in allocated:
      if not isinstance(item, dict):
        continue
      else:
        item = cast(dict[str, Any], item)
      
      key = safe_get_string(item, "type")
      value = safe_get_float(item, "count")
      
      allocated_resource_counts[key] = value
    
    return SlurmAccountingResult(job_id, start, end, allocated_resource_counts)