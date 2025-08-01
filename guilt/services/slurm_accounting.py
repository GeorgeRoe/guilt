from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from typing import Any, cast
import subprocess
import json

class SlurmAccountingService(SlurmAccountingServiceInterface):
  def _run_sacct_command(self, parameters: dict[str, Any]) -> list[LazySlurmAccountingResult]:
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
    
    raw_data = JsonReader.expect_dict(cast(Json, json.loads(result.stdout.strip())))
    
    jobs_data = JsonReader.ensure_get_list(raw_data, "jobs")

    return [LazySlurmAccountingResult(JsonReader.expect_dict(job_data)) for job_data in jobs_data]
  
  def get_jobs_with_ids(self, ids: list[str]) -> list[LazySlurmAccountingResult]:
    return self._run_sacct_command({
      "jobs": ids,
    })

  def get_jobs_submitted_by_username(self, user: str) -> list[LazySlurmAccountingResult]:
    return self._run_sacct_command({
      "user": user,
      "starttime": "1970-01-01"
    })