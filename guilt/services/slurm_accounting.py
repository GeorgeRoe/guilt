import subprocess
from guilt.log import logger
import json
from datetime import datetime, timezone

class SlurmAccountingResult:
  def __init__(self, job_id, start_time, end_time, resources):
    self.job_id = job_id
    self.start_time = start_time
    self.end_time = end_time
    self.resources = resources
  
  @classmethod
  def fromDict(cls, data: dict):
    return cls(
      data.get("job_id"),
      datetime.fromtimestamp(data.get("time").get("start")).replace(tzinfo=timezone.utc),
      datetime.fromtimestamp(data.get("time").get("end")).replace(tzinfo=timezone.utc),
      {item.get("type"): item.get("count") for item in data.get("tres").get("allocated")}
    )
    
  def __repr__(self):
    return (
        f"SlurmAccountingResult(job_id={self.job_id}, "
        f"start_time={self.start_time}, "
        f"end_time={self.end_time}, "
        f"resources={self.resources})"
    )

class SlurmAccountingService:
  @classmethod
  def getJobs(cls, ids):
    return cls.fetchData({
      "jobs": ids,
    })
    
  @classmethod
  def getAllJobsForUser(cls, user):
    return cls.fetchData({
      "user": user,
      "starttime": "1970-01-01"
    })

  @classmethod
  def fetchData(cls, options):
    options["json"] = True
    result = cls.runCommand(options)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    raw_data = json.loads(result.stdout.strip())
    
    jobs_data = raw_data.get("jobs")
    
    return [SlurmAccountingResult.fromDict(job_data) for job_data in jobs_data]
    
  @classmethod
  def runCommand(cls, options):
    command = ["sacct"]
    
    for key, value in options.items():
      command.append("--" + key)
      
      if isinstance(value, list):
        command.append(",".join([str(item) for item in value]))
      elif not isinstance(value, bool):
        command.append(str(value))
        
    logger.info(f"Running command: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True)