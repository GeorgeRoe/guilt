from guilt.config.cpu_profiles import CpuProfile
from pathlib import Path
import json

PATH = Path.home() / ".guilt" / "unprocessed_jobs.json"

class UnprocessedJob:
  def __init__(self, job_id: int, cpu_profile: CpuProfile):
    self.job_id = int(job_id)
    self.cpu_profile = cpu_profile

  def __repr__(self):
    return (
        f"UnprocessedJob(job_id={self.job_id}, "
        f"cpu_profile={self.cpu_profile})"
    )
    
  @classmethod
  def from_dict(cls, data: dict):
    return cls(data.get("job_id"), CpuProfile.from_dict(data.get("cpu_profile")))
  
  def to_dict(self) -> dict:
    return {
      "job_id": self.job_id,
      "cpu_profile": self.cpu_profile.to_dict()
    }

class UnprocessedJobsData:
  def __init__(self):
    data = {}
    
    if PATH.exists():
      with PATH.open("r") as file:
        data = json.load(file)

    self.jobs = {}
    for job_id, unprocessed_job in data.items():
      data = {
        "job_id": job_id,
        **unprocessed_job
      }
      self.jobs[job_id] = UnprocessedJob.from_dict(data)
    
  def add_job(self, job: UnprocessedJob) -> bool:
    if job.job_id in self.jobs:
      return False
    
    self.jobs[job.job_id] = job
    
  def remove_job(self, job_id: str) -> bool:
    if str(job_id) in self.jobs:
      del self.jobs[str(job_id)]
      return True
    
    return False

  def save(self):    
    data = {
      job.job_id: {k: v for k, v in job.to_dict().items() if k != "job_id"}
      for job in self.jobs.values()
    }
    
    PATH.parent.mkdir(parents=True, exist_ok=True)

    with PATH.open("w") as file:
      json.dump(data, file, indent=2)