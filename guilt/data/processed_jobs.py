from datetime import datetime
from guilt.config.cpu_profiles import CpuProfile
from pathlib import Path
import json

PATH = Path.home() / ".guilt" / "processed_jobs.json"

class ProcessedJob:
  def __init__(self, start: datetime, end: datetime, job_id: int, cpu_profile: CpuProfile, energy: float, emissions: float, generation_mix: dict):
    self.start = start
    self.end = end
    self.job_id = job_id
    self.cpu_profile = cpu_profile
    self.energy = energy
    self.emissions = emissions
    self.generation_mix = generation_mix
    
  @classmethod
  def from_dict(cls, data: dict):
    return cls(
      datetime.fromisoformat(data.get("start")),
      datetime.fromisoformat(data.get("end")),
      data.get("job_id"),
      CpuProfile.from_dict(data.get("cpu_profile")),
      data.get("energy"),
      data.get("emissions"),
      data.get("generation_mix")
    )
    
  def to_dict(self) -> dict:
    return {
      "start": self.start.isoformat(),
      "end": self.end.isoformat(),
      "job_id": self.job_id,
      "cpu_profile": self.cpu_profile.to_dict(),
      "energy": self.energy,
      "emissions": self.emissions,
      "generation_mix": self.generation_mix
    }

class ProcessedJobsData:
  def __init__(self):
    data = {}
    
    if PATH.exists():
      with PATH.open("r") as file:
        data = json.load(file)

    self.jobs = {}
    for job_id, processed_job in data.items():
      data = {
        "job_id": job_id,
        **processed_job
      }
      self.jobs[job_id] = ProcessedJob.from_dict(data)

  def add_job(self, job: ProcessedJob) -> bool:
    if job.job_id in self.jobs:
      return False
    
    self.jobs[job.job_id] = job
    return True

  def save(self):    
    data = {
      job.job_id: {k: v for k, v in job.to_dict().items() if k != "job_id"}
      for job in self.jobs.values()
    }
    
    PATH.parent.mkdir(parents=True, exist_ok=True)

    with PATH.open("w") as file:
      json.dump(data, file, indent=2)
    