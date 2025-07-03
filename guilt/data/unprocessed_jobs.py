from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.cpu_profile import MapToCpuProfile
from dataclasses import asdict
from pathlib import Path
import json
from guilt.log import logger
from typing import Any
from guilt.utility.safe_get import safe_get_string, safe_get_dict

PATH = Path.home() / ".guilt" / "unprocessed_jobs.json"

class UnprocessedJob:
  def __init__(self, job_id: str, cpu_profile: CpuProfile) -> None:
    self.job_id = job_id
    self.cpu_profile = cpu_profile

  def __repr__(self) -> str:
    return (
        f"UnprocessedJob(job_id={self.job_id}, "
        f"cpu_profile={self.cpu_profile})"
    )
    
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "UnprocessedJob":
    logger.debug(f"Deserializing ProcessedJob: {data}")
    
    job_id = safe_get_string(data, "job_id")
    cpu_profile = MapToCpuProfile.from_json_file_contents(safe_get_dict(data, "cpu_profile"))
    
    return cls(job_id, cpu_profile)
  
  def to_dict(self) -> dict[str, Any]:
    return {
      "job_id": self.job_id,
      "cpu_profile": asdict(self.cpu_profile)
    }

class UnprocessedJobsData:
  def __init__(self, jobs: dict[str, UnprocessedJob]) -> None:
    self.jobs = jobs
    
  def to_dict(self) -> dict[str, Any]:
    return {
      job.job_id: {k: v for k, v in job.to_dict().items() if k != "job_id"}
      for job in self.jobs.values()
    }
    
  @classmethod
  def get_default(cls) -> "UnprocessedJobsData":
    return cls({})
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "UnprocessedJobsData":
    jobs: dict[str, UnprocessedJob] = {}
    
    for job_id, unprocessed_job in data.items():
      jobs[job_id] = UnprocessedJob.from_dict({ "job_id": job_id, **unprocessed_job })

    return cls(jobs)
  
  @classmethod
  def from_file(cls, path: Path = PATH) -> "UnprocessedJobsData":
    data = None
    
    if path.exists():
      try:
        with path.open("r") as file:
          data = json.load(file)
        logger.info(f"Loaded {len(data)} unprocessed jobs from {path}")
      except Exception as e:
        logger.error(f"Failed to load unprocessed jobs from {path}: {e}")
    else:
      logger.warning("No unprocessed jobs file found, starting with empty dataset")

    return cls.get_default() if data is None else cls.from_dict(data)

  def add_job(self, job: UnprocessedJob) -> bool:
    if job.job_id in self.jobs:
      logger.warning(f"Job ID {job.job_id} already exists in unprocessed jobs")
      return False
    
    self.jobs[job.job_id] = job
    logger.info(f"Added unprocessed job ID {job.job_id}")
    return True
    
  def remove_job(self, job_id: str) -> bool:
    if str(job_id) in self.jobs:
      del self.jobs[str(job_id)]
      logger.info(f"Removed unprocessed job ID {job_id}")
      return True
    
    logger.warning(f"Job ID {job_id} doesn't exist in unprocessed jobs")
    return False

  def save(self) -> None:
    PATH.parent.mkdir(parents=True, exist_ok=True)
    
    data = self.to_dict()

    try:
      with PATH.open("w") as file:
        json.dump(data, file, indent=2)
      logger.info(f"Saved {len(data)} unprocessed jobs to {PATH}")
    except Exception as e:
      logger.error(f"Failed to save unprocessed jobs to {PATH}: {e}")