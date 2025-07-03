from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.utility.safe_get import safe_get_dict
from typing import Any

class MapToUnprocessedJobsData:
  @staticmethod
  def from_json_file_contents(data: dict[str, Any]) -> UnprocessedJobsData:
    return UnprocessedJobsData({
      job_id: UnprocessedJob(
        job_id,
        MapToCpuProfile.from_json_file_contents(safe_get_dict(values, "cpu_profile"))
      )
      for job_id, values in data.items()
    })