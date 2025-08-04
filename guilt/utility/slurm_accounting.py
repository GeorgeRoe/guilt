from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json
from typing import Optional, Sequence, cast
from datetime import datetime
import subprocess
import json

def run(
  job_ids: Optional[list[str]] = None,
  user: Optional[str] = None,
  since: Optional[datetime] = None
) -> Sequence[LazySlurmAccountingResult]:
  command = ["sacct", "--json"]

  if job_ids:
    command.append("--jobs")
    command.append(",".join(job_ids))

  if user:
    command.append("--user")
    command.append(user)

  if since:
    command.append("--starttime")
    command.append(since.strftime("%Y-%m-%dT%H:%M:%S"))

  result = subprocess.run(command, capture_output=True, text=True)

  if result.returncode != 0:
    raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")

  raw_data = JsonReader.expect_dict(cast(Json, json.loads(result.stdout.strip())))

  jobs_data = JsonReader.ensure_get_list(raw_data, "jobs")

  return [LazySlurmAccountingResult(JsonReader.expect_dict(job_data)) for job_data in jobs_data]