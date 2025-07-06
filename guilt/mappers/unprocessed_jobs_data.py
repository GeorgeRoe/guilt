from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader

class MapToUnprocessedJobsData:
  @staticmethod
  def from_json(data: Json) -> UnprocessedJobsData:
    return UnprocessedJobsData({
      job_id: UnprocessedJob(
        job_id,
        MapToCpuProfile.from_json(JsonReader.ensure_get_json(JsonReader.expect_dict(values), "cpu_profile"))
      )
      for job_id, values in JsonReader.expect_dict(data).items()
    })