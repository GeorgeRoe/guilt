from guilt.data.unprocessed_jobs import UnprocessedJobsData
from guilt.data.processed_jobs import ProcessedJobsData, ProcessedJob
from guilt.ip_info import IpInfo
from guilt.carbon_dioxide_forecast import CarbonDioxideForecast
from guilt.utility.format_grams import format_grams
import subprocess
import json
from datetime import datetime, timedelta, timezone
import plotext as plt
import shutil
from guilt.log import logger

def process_cmd(_):
  unprocessed_jobs_data = UnprocessedJobsData()
  processed_jobs_data = ProcessedJobsData()
  
  jobs = unprocessed_jobs_data.jobs.values()
  
  job_ids = [job.job_id for job in jobs]
  
  command = ["sacct", "--jobs", ",".join([str(job_id) for job_id in job_ids]), "--json"]
  logger.info(f"Running command: {' '.join(command)}")
  try:
    result = subprocess.run(command, capture_output=True, text=True)
  except Exception as e:
    logger.error(f"Error running command '{' '.join(command)}': {e}")
    return
  
  if result.returncode != 0:
    logger.error(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    return
  
  raw_sacct_data = json.loads(result.stdout.strip())
  sacct_data = {item.get("job_id"): item for item in raw_sacct_data.get("jobs")}
  
  ip_info = IpInfo()
  
  for job in jobs:
    job_sacct = sacct_data.get(job.job_id)
    
    start_time = datetime.fromtimestamp(job_sacct.get("time").get("start")).replace(tzinfo=timezone.utc)
    end_time = datetime.fromtimestamp(job_sacct.get("time").get("end")).replace(tzinfo=timezone.utc)
    
    logger.debug(f"Collected job start and end time: {start_time} -> {end_time}")
        
    cpu_tres = next((item for item in job_sacct.get("tres").get("allocated") if item.get("type") == "cpu"), None)
    if cpu_tres is None:
      logger.warning(f"Failed to read CPU allocation for job with id '{job.job_id}', skipping this job")
      continue
    
    allocated_cpu = cpu_tres.get("count")
    
    wattage = allocated_cpu * job.cpu_profile.tdp_per_core
    
    buffer = timedelta(minutes=30)
    forecast_start = start_time - buffer
    forecast_end = end_time + buffer

    forecast = CarbonDioxideForecast(forecast_start, forecast_end, ip_info.postal)
    
    emissions = 0.0 # kg of CO2
    kwh = 0.0
    
    total_mix = {}
    total_mix_seconds = 0.0
    
    for entry in forecast.entries:
      entry_start = datetime.fromisoformat(entry.from_time.replace("Z", "+00:00"))
      entry_end = datetime.fromisoformat(entry.to_time.replace("Z", "+00:00"))
      overlap_start = max(start_time, entry_start)
      overlap_end = min(end_time, entry_end)
      overlap_duration = (overlap_end - overlap_start).total_seconds()
      
      if overlap_duration > 0:
        overlap_hours = overlap_duration / 3600
        overlap_kwh = (wattage * overlap_hours) / 1000
        kwh += overlap_kwh
        emissions += overlap_kwh * entry.intensity.forecast
        
        for source, percent in entry.generationmix.items():
          total_mix[source] = total_mix.get(source, 0) + percent * overlap_duration
        total_mix_seconds += overlap_duration
    
    average_mix = {k: v / total_mix_seconds for k, v in total_mix.items()}
    
    print(f"{job.job_id} -> energy usage: {kwh:.2e} kWh, emissions: {format_grams(emissions)} of CO2")

    processed_job = ProcessedJob(
      start_time,
      end_time,
      job.job_id,
      job.cpu_profile,
      kwh,
      emissions,
      average_mix
    )
    
    if not processed_jobs_data.add_job(processed_job):
      logger.error("Failed to add processed jobs")
      continue
    
  for job_id in job_ids:
    if not unprocessed_jobs_data.remove_job(job_id):
      logger.error(f"Unable to remove job with id '{job_id}'")
      return
        
  unprocessed_jobs_data.save()
  processed_jobs_data.save()