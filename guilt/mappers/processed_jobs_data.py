from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.utility.safe_get import safe_get_string, safe_get_dict, safe_get_float
from typing import Any
from datetime import datetime

class MapToProcessedJobsData:
  @staticmethod
  def from_json_file_contents(data: dict[str, Any]) -> ProcessedJobsData:
    return ProcessedJobsData({
      job_id: ProcessedJob(
        datetime.fromisoformat(safe_get_string(values, "start")),
        datetime.fromisoformat(safe_get_string(values, "end")),
        job_id,
        MapToCpuProfile.from_json_file_contents(safe_get_dict(values, "cpu_profile")),
        safe_get_float(values, "energy"),
        safe_get_float(values, "emissions"),
        {source: float(percentage) for source, percentage in safe_get_dict(values, "generation_mix").items()}
      )
      for job_id, values in data.items()
    })