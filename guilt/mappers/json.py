from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from typing import cast
from guilt.types.json import Json
from dataclasses import asdict
import json

class MapToJson:
  @staticmethod
  def from_cpu_profile(cpu_profile: CpuProfile) -> dict[str, Json]:
    return cast(dict[str, Json], {
      "name": cpu_profile.name,
      "tdp": cpu_profile.tdp,
      "cores": cpu_profile.cores
    })
  
  @classmethod
  def from_cpu_profiles_config(cls, cpu_profiles_config: CpuProfilesConfig) -> dict[str, Json]:
    return cast(dict[str, Json], {
      "default": cpu_profiles_config.default.name,
      "profiles": {
        profile.name: {key: value for key, value in cls.from_cpu_profile(profile).items() if key != "name"}
        for profile in cpu_profiles_config.profiles.values()
      }
    })
    
  @staticmethod
  def from_processed_jobs_data(processed_jobs_data: ProcessedJobsData) -> dict[str, Json]:
    return cast(dict[str, Json], {
      job_id: {
        "start": processed_job.start.isoformat(),
        "end": processed_job.end.isoformat(),
        "cpu_profile": asdict(processed_job.cpu_profile),
        "energy": processed_job.energy,
        "emissions": processed_job.emissions,
        "generation_mix": processed_job.generation_mix
      }
      for job_id, processed_job in processed_jobs_data.jobs.items()
    })
  
  @staticmethod
  def from_unprocessed_jobs_data(unprocessed_jobs_data: UnprocessedJobsData) -> dict[str, Json]:
    return cast(dict[str, Json], {
      job_id: {key: value for key, value in asdict(unprocessed_job).items() if key != "job_id"}
      for job_id, unprocessed_job in unprocessed_jobs_data.jobs.items() 
    })
    
  @staticmethod
  def from_directive_lines(lines: list[str], directive_comment: str) -> dict[str, Json]:
    directives: dict[str, Json] = {}
    for line in lines:
      if line.startswith(directive_comment):
        directive = line.replace(directive_comment, "").replace("--", "").split("=")
        key = directive[0].strip()
        value_str = directive[1].strip()

        value: Json = None
        if value_str:
          value = cast(Json, json.loads(value_str))
        else:
          value = True
        
        directives[key] = value
        
    return directives