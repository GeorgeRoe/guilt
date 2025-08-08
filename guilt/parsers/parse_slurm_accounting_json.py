from guilt.types.json import Json
from guilt.utility import json_reader
from datetime import datetime, timezone

def get_job_id(data: dict[str, Json]) -> str:
  return str(json_reader.ensure_get_json(data, "job_id"))

def get_start_time(data: dict[str, Json]) -> datetime:
  time_data = json_reader.ensure_get_dict(data, "time")
  return datetime.fromtimestamp(float(json_reader.ensure_get_number(time_data, "start")))

def get_end_time(data: dict[str, Json]) -> datetime:
  time_data = json_reader.ensure_get_dict(data, "time")
  return datetime.fromtimestamp(float(json_reader.ensure_get_number(time_data, "end")))

def get_resources(data: dict[str, Json]) -> dict[str, float]:
  tres_data = json_reader.ensure_get_dict(data, "tres")
  allocated = json_reader.ensure_get_list(tres_data, "allocated")

  resource_to_count_map: dict[str, float] = {}
  for item in allocated:
    item_data = json_reader.expect_dict(item)
    resource_type = json_reader.ensure_get_str(item_data, "type")
    count = float(json_reader.ensure_get_number(item_data, "count"))
    resource_to_count_map[resource_type] = count

  return resource_to_count_map