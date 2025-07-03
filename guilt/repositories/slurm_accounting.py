import subprocess
from guilt.log import logger
import json
from typing import Union
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.mappers.slurm_accounting_result import MapToSlurmAccountingResult

CommandParameters = dict[str, Union[str, int, float, list[str], list[int], list[float]]]

class SlurmAccountingRepository:
  def getJobs(self, ids: list[str]) -> list[SlurmAccountingResult]:
    return self.fetchData({
      "jobs": ids,
    })
    
  def getAllJobsForUser(self, user: str) -> list[SlurmAccountingResult]:
    return self.fetchData({
      "user": user,
      "starttime": "1970-01-01"
    })

  def fetchData(self, options: CommandParameters) -> list[SlurmAccountingResult]:
    options["json"] = True
    result = self.runCommand(options)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    raw_data = json.loads(result.stdout.strip())
    
    jobs_data = raw_data.get("jobs")
    if jobs_data is None:
      raise ValueError("Jobs is required.")

    return [MapToSlurmAccountingResult.from_command_dict(job_data) for job_data in jobs_data]
    
  def runCommand(self, options: CommandParameters):
    command = ["sacct"]
    
    for key, value in options.items():
      command.append("--" + key)
      
      if isinstance(value, list):
        command.append(",".join([str(item) for item in value]))
      elif not isinstance(value, bool):
        command.append(str(value))
        
    logger.info(f"Running command: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True)