from guilt.data.unprocessed_jobs import UnprocessedJobsData, UnprocessedJob
from guilt.config.cpu_profiles import CpuProfilesConfig
from guilt.log import logger
import json
import subprocess
import os

def backfill_cmd(_):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
  
  command = ["sacct", "-S", "1970-01-01", "-u", user, "--json"]
  logger.info(f"Running command: {' '.join(command)}")
  try:
    result = subprocess.run(command, capture_output=True, text=True)
  except Exception as e:
    logger.error(f"Error running command '{' '.join(command)}': {e}")
    return
  
  if result.returncode != 0:
    logger.error(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    return
  
  job_ids = [job.get("job_id") for job in json.loads(result.stdout.strip()).get("jobs")]
  
  unprocessed_jobs_data = UnprocessedJobsData()
  cpu_profiles_config = CpuProfilesConfig()
  
  for job_id in job_ids:
    unprocessed_jobs_data.add_job(UnprocessedJob(
      int(job_id),
      cpu_profiles_config.default
    ))
    
  unprocessed_jobs_data.save()