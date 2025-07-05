from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.mappers import map_to
from typing import Any, cast
import subprocess
import json

class SlurmAccountingService(SlurmAccountingServiceInterface):
  def _run_sacct_command(self, parameters: dict[str, Any]) -> list[SlurmAccountingResult]:
    command = ["sacct"]
    
    parameters["json"] = True
    for key, value in parameters.items():
      command.append("--" + key)
      
      if isinstance(value, list):
        command.append(",".join([str(item) for item in cast(list[Any], value)]))
      elif not isinstance(value, bool):
        command.append(str(value))

    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    raw_data = json.loads(result.stdout.strip())
    
    jobs_data = raw_data.get("jobs")
    if jobs_data is None:
      raise ValueError("Jobs is required.")

    return [map_to.slurm_accounting_result.from_command_dict(job_data) for job_data in jobs_data]
  
  def get_jobs_with_ids(self, ids: list[str]) -> list[SlurmAccountingResult]:
    return self._run_sacct_command({
      "jobs": ids,
    })

  def get_users_jobs(self, user: str) -> list[SlurmAccountingResult]:
    return self._run_sacct_command({
      "user": user,
      "starttime": "1970-01-01"
    })