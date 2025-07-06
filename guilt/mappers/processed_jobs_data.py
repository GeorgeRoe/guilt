from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from datetime import datetime

class MapToProcessedJobsData:
  @staticmethod
  def from_json(data: Json) -> ProcessedJobsData:
    data = JsonReader.expect_dict(data)
    
    processed_jobs: list[ProcessedJob] = []
    for job_id, processed_job_values  in data.items():
      processed_job_data = JsonReader.expect_dict(processed_job_values)
      
      start = datetime.fromisoformat(JsonReader.ensure_get_str(processed_job_data, "start"))
      end = datetime.fromisoformat(JsonReader.ensure_get_str(processed_job_data, "end"))
      cpu_profile = MapToCpuProfile.from_json(JsonReader.ensure_get_dict(processed_job_data, "cpu_profile"))
      energy = float(JsonReader.ensure_get_number(processed_job_data, "energy"))
      emissions = float(JsonReader.ensure_get_number(processed_job_data, "emissions"))
      generation_mix = {source: float(JsonReader.expect_number(percentage)) for source, percentage in JsonReader.ensure_get_dict(processed_job_data, "generation_mix").items()}
    
      processed_jobs.append(ProcessedJob(
        start,
        end,
        job_id,
        cpu_profile,
        energy,
        emissions,
        generation_mix
      ))
    
    return ProcessedJobsData({processed_job.job_id: processed_job for processed_job in processed_jobs})