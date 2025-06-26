import subprocess
from guilt.log import logger
import json
from datetime import datetime, timezone
from guilt.utility.safe_get import safe_get_string, safe_get_float, safe_get_dict, safe_get_list
from typing import Any, cast, Union

CommandParameters = dict[str, Union[str, int, float, list[str], list[int], list[float]]]

class SlurmAccountingResult:
  def __init__(self, job_id: str, start_time: datetime, end_time: datetime, resources: dict[str, float]) -> None:
    self.job_id = job_id
    self.start_time = start_time
    self.end_time = end_time
    self.resources = resources
  
  @classmethod
  def fromDict(cls, data: dict[str, Any]) -> "SlurmAccountingResult":
    job_id = safe_get_string(data, "job_id")
        
    time = safe_get_dict(data, "time")

    start = datetime.fromtimestamp(safe_get_float(time, "start")).replace(tzinfo=timezone.utc)
    end = datetime.fromtimestamp(safe_get_float(time, "end")).replace(tzinfo=timezone.utc)
    
    resources = data.get("tres")
    if resources is None:
      raise ValueError("Tres is required.")
    
    resources = safe_get_dict(data, "tres")
    allocated = safe_get_list(resources, "allocated")
    
    allocated_resource_counts: dict[str, float] = {}
    for item in allocated:
      if not isinstance(item, dict):
        continue
      else:
        item = cast(dict[str, Any], item)
      
      key = safe_get_string(item, "type")
      value = safe_get_float(item, "count")
      
      allocated_resource_counts[key] = value
    
    return cls(job_id, start, end, allocated_resource_counts)
    
  def __repr__(self) -> str:
    return (
        f"SlurmAccountingResult(job_id={self.job_id}, "
        f"start_time={self.start_time}, "
        f"end_time={self.end_time}, "
        f"resources={self.resources})"
    )

class SlurmAccountingService:
  @classmethod
  def getJobs(cls, ids: list[str]) -> list[SlurmAccountingResult]:
    return cls.fetchData({
      "jobs": ids,
    })
    
  @classmethod
  def getAllJobsForUser(cls, user: str) -> list[SlurmAccountingResult]:
    return cls.fetchData({
      "user": user,
      "starttime": "1970-01-01"
    })

  @classmethod
  def fetchData(cls, options: CommandParameters) -> list[SlurmAccountingResult]:
    options["json"] = True
    result = cls.runCommand(options)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    raw_data = json.loads(result.stdout.strip())
    
    jobs_data = raw_data.get("jobs")
    if jobs_data is None:
      raise ValueError("Jobs is required.")

    return [SlurmAccountingResult.fromDict(job_data) for job_data in jobs_data]
    
  @classmethod
  def runCommand(cls, options: CommandParameters):
    command = ["sacct"]
    
    for key, value in options.items():
      command.append("--" + key)
      
      if isinstance(value, list):
        command.append(",".join([str(item) for item in value]))
      elif not isinstance(value, bool):
        command.append(str(value))
        
    logger.info(f"Running command: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True)