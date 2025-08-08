from guilt.interfaces.repositories.processed_jobs import ProcessedJobsRepositoryInterface
from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.interfaces.models.processed_job import ProcessedJobInterface
from guilt.models.lazy_json_processed_job import LazyJsonProcessedJob
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json
from typing import Optional, Sequence, cast
from pathlib import Path
import json

class JsonProcessedJobsRepository(ProcessedJobsRepositoryInterface):
  def __init__(
    self,
    path: Path,
    cpu_profiles_repository: CpuProfilesRepositoryInterface
  ) -> None:
    self._path = path
    self._cpu_profiles_repository = cpu_profiles_repository

    self._jobs: dict[str, ProcessedJobInterface] = {}
    with self._path.open("r") as file:
      raw_jobs = JsonReader.expect_list(json.load(file))
      for raw_job in raw_jobs:
        job = JsonReader.expect_dict(raw_job)

        cpu_profile = self._cpu_profiles_repository.get(
          JsonReader.ensure_get_str(job, "cpu_profile_name")
        )

        if cpu_profile is None:
          raise ValueError(
            f"CPU profile with ID {JsonReader.ensure_get_str(job, 'cpu_profile_name')} not found."
          ) 

        processed_job = LazyJsonProcessedJob(
          job,
          cpu_profile
        )

        self._jobs[processed_job.job_id] = processed_job
  
  def get(self, job_id: str) -> Optional[ProcessedJobInterface]:
    return self._jobs.get(job_id)
  
  def get_all(self) -> Sequence[ProcessedJobInterface]:
    return list(self._jobs.values())

  def upsert(self, job: ProcessedJobInterface) -> None:
    self._jobs[job.job_id] = job

  def delete(self, job_id: str) -> None:
    if job_id in self._jobs:
      del self._jobs[job_id]

  def save(self) -> bool:
    raw_jobs: list[dict[str, Json]] = []

    for job in self._jobs.values():
      raw_jobs.append({
        "start": job.start.isoformat(),
        "end": job.end.isoformat(),
        "job_id": job.job_id,
        "cpu_profile_name": job.cpu_profile.name,
        "energy": job.energy,
        "emissions": job.emissions,
        "generation_mix": cast(dict[str, Json], job.generation_mix)
      })

    try:
      with self._path.open("w") as file:
        json.dump(raw_jobs, file, indent=2)
      return True
    except Exception:
      return False