from datetime import datetime
from guilt.config.cpu_profiles import CpuProfile
from pathlib import Path
import json
from guilt.log import logger
from typing import Any, cast
from guilt.utility.safe_get import safe_get_string, safe_get_dict, safe_get_float

PATH = Path.home() / ".guilt" / "processed_jobs.json"

class ProcessedJob:
  def __init__(self, start: datetime, end: datetime, job_id: str, cpu_profile: CpuProfile, energy: float, emissions: float, generation_mix: dict[str, float]):
    self.start = start
    self.end = end
    self.job_id = job_id
    self.cpu_profile = cpu_profile
    self.energy = energy
    self.emissions = emissions
    self.generation_mix = generation_mix
    
  @classmethod
  def from_dict(cls, data: dict[str, Any]):
    logger.debug(f"Deserializing ProcessedJob: {data}")
    
    start = datetime.fromisoformat(safe_get_string(data, "start"))
    end = datetime.fromisoformat(safe_get_string(data, "end"))
    job_id = safe_get_string(data, "job_id")
    cpu_profile = CpuProfile.from_dict(safe_get_dict(data, "cpu_profile"))
    energy = safe_get_float(data, "energy")
    emissions = safe_get_float(data, "emissions")
    generation_mix = cast(dict[str, float], safe_get_dict(data, "generation_mix"))
    
    return cls(start, end, job_id, cpu_profile, energy, emissions, generation_mix)
    
  def to_dict(self) -> dict[str, Any]:
    return {
      "start": self.start.isoformat(),
      "end": self.end.isoformat(),
      "job_id": self.job_id,
      "cpu_profile": self.cpu_profile.to_dict(),
      "energy": self.energy,
      "emissions": self.emissions,
      "generation_mix": self.generation_mix
    }
  
  def __repr__(self) -> str:
    return (
        f"ProcessedJob(start={self.start}, "
        f"end={self.end}, "
        f"job_id={self.job_id}, "
        f"cpu_profile={self.cpu_profile}, "
        f"energy={self.energy} kWh, "
        f"emissions={self.emissions} grams, "
        f"generation_mix={self.generation_mix})"
    )

class ProcessedJobsData:
  def __init__(self, jobs: dict[str, ProcessedJob]) -> None:
    self.jobs = jobs
    
  def to_dict(self) -> dict[str, Any]:
    return {
      job.job_id: {k: v for k, v in job.to_dict().items() if k != "job_id"}
      for job in self.jobs.values()
    }
  
  @classmethod
  def get_default(cls) -> "ProcessedJobsData":
    return cls({})
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "ProcessedJobsData":
    jobs: dict[str, ProcessedJob] = {}
    
    for job_id, processed_job in data.items():
      jobs[job_id] = ProcessedJob.from_dict({ "job_id": job_id, **processed_job})
      
    return cls(jobs)
  
  @classmethod
  def from_file(cls, path: Path = PATH) -> "ProcessedJobsData":
    data = None
    
    if path.exists():
      try:
        with path.open("r") as file:
          data = json.load(file)
        logger.info(f"Loaded {len(data)} processed jobs from {path}")
      except Exception as e:
        logger.error(f"Failed to load processed jobs from {path}: {e}")
    else:
      logger.warning("No processed jobs file found, starting with empty dataset")
      
    return cls.get_default() if data is None else cls.from_dict(data)

  def add_job(self, job: ProcessedJob) -> bool:
    if job.job_id in self.jobs:
      logger.warning(f"Job ID {job.job_id} already exists in processed jobs")
      return False
    
    self.jobs[job.job_id] = job
    logger.info(f"Added processed job ID {job.job_id}")
    return True

  def save(self) -> None:  
    PATH.parent.mkdir(parents=True, exist_ok=True)

    data = self.to_dict()

    try:
      with PATH.open("w") as file:
        json.dump(data, file, indent=2)
      logger.info(f"Saved {len(data)} processed jobs to {PATH}")
    except Exception as e:
      logger.error(f"Failed to save processed jobs to {PATH}: {e}")
    