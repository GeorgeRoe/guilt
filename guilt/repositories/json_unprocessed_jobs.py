from guilt.interfaces.repositories.unprocessed_jobs import UnprocessedJobsRepositoryInterface
from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.interfaces.models.unprocessed_job import UnprocessedJobInterface
from guilt.models.lazy_json_unprocessed_job import LazyJsonUnprocessedJob
from guilt.utility import json_reader
from guilt.types.json import Json
from typing import Optional, Sequence, cast
from pathlib import Path
import json

class JsonUnprocessedJobsRepository(UnprocessedJobsRepositoryInterface):
  def __init__(
    self,
    path: Path,
    cpu_profiles_repository: CpuProfilesRepositoryInterface
  ) -> None:
    self._path = path
    self._cpu_profiles_repository = cpu_profiles_repository

    self._jobs: dict[str, UnprocessedJobInterface] = {}
    with self._path.open("r") as file:
      raw_jobs = json_reader.expect_list(json.load(file))

      for raw_job in raw_jobs:
        job = json_reader.expect_dict(raw_job)

        cpu_profile = self._cpu_profiles_repository.get(
          json_reader.ensure_get_str(job, "cpu_profile_name")
        )

        if cpu_profile is None:
          raise ValueError(
            f"CPU profile with ID {json_reader.ensure_get_str(job, 'cpu_profile_name')} not found."
          ) 

        unprocessed_job = LazyJsonUnprocessedJob(
          job,
          cpu_profile
        )

        self._jobs[unprocessed_job.job_id] = unprocessed_job

  def get(self, job_id: str) -> Optional[UnprocessedJobInterface]:
    return self._jobs.get(job_id)
  
  def get_all(self) -> Sequence[UnprocessedJobInterface]:
    return list(self._jobs.values())
  
  def upsert(self, job: UnprocessedJobInterface) -> None:
    self._jobs[job.job_id] = job

  def delete(self, job_id: str) -> None:
    if job_id in self._jobs:
      del self._jobs[job_id]
      print(len(self._jobs.keys()))

  def save(self) -> bool:
    raw_jobs: list[dict[str, Json]] = []

    for job in self._jobs.values():
      raw_jobs.append({
        "job_id": job.job_id,
        "cpu_profile_name": job.cpu_profile.name
      })

    try:
      with self._path.open("w") as file:
        json.dump(raw_jobs, file, indent=2)
      return True
    except Exception as e:
      return False