from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from typing import Any
from dataclasses import asdict

class MapToJsonFileContents:
  @staticmethod
  def from_cpu_profiles_config(cpu_profiles_config: CpuProfilesConfig) -> dict[str, Any]:   
    return {
      "default": cpu_profiles_config.default.name,
      "profiles": {
        profile.name: {key: value for key, value in asdict(profile).items() if key != "name"}
        for profile in cpu_profiles_config.profiles.values()
      }
    }
    
  @staticmethod
  def from_processed_jobs_data(processed_jobs_data: ProcessedJobsData) -> dict[str, Any]:
    return {
      job_id: {
        "start": processed_job.start.isoformat(),
        "end": processed_job.end.isoformat(),
        "cpu_profile": asdict(processed_job.cpu_profile),
        "energy": processed_job.energy,
        "emissions": processed_job.emissions,
        "generation_mix": processed_job.generation_mix
      }
      for job_id, processed_job in processed_jobs_data.jobs.items()
    }
  
  @staticmethod
  def from_unprocessed_jobs_data(unprocessed_jobs_data: UnprocessedJobsData) -> dict[str, Any]:
    return {
      job_id: {key: value for key, value in asdict(unprocessed_job).items() if key != "job_id"}
      for job_id, unprocessed_job in unprocessed_jobs_data.jobs.items() 
    }