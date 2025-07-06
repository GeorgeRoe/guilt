from datetime import datetime, timezone
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from guilt.models.slurm_accounting_result import SlurmAccountingResult

class MapToSlurmAccountingResult:
  @staticmethod
  def from_json(data: Json) -> SlurmAccountingResult:
    data = JsonReader.expect_dict(data)
    
    job_id = JsonReader.ensure_get_str(data, "job_id")
    
    time_data = JsonReader.ensure_get_dict(data, "time")
    start = datetime.fromtimestamp(float(JsonReader.ensure_get_number(time_data, "start"))).replace(tzinfo=timezone.utc)
    end = datetime.fromtimestamp(float(JsonReader.ensure_get_number(time_data, "end"))).replace(tzinfo=timezone.utc)
  
    resources = JsonReader.ensure_get_dict(data, "tres")
    allocated = JsonReader.ensure_get_list(resources, "allocated")
    
    allocated_resource_counts: dict[str, float] = {}
    for item in allocated:
      item_data = JsonReader.expect_dict(item)
      
      key = JsonReader.ensure_get_str(item_data, "type")
      value = float(JsonReader.ensure_get_number(item_data, "count"))
      
      allocated_resource_counts[key] = value    
  
    return SlurmAccountingResult(job_id, start, end, allocated_resource_counts)