from guilt.data.unprocessed_jobs import UnprocessedJobsData
from guilt.ip_info import IpInfo
from guilt.carbon_dioxide_forecast import CarbonDioxideForecast
from guilt.utility.format_grams import format_grams
import subprocess
import json
from datetime import datetime, timedelta, timezone

def process_cmd(_):  
  jobs =  UnprocessedJobsData().jobs.values()
  
  job_ids = [job.job_id for job in jobs]
  
  command = ["sacct", "--jobs", ",".join([str(job_id) for job_id in job_ids]), "--json"]
  result = subprocess.run(command, capture_output=True, text=True)
  
  if result.returncode != 0:
    print(f"The command '{' '.join(command)}' encountered an error:")
    print(result.stderr)
    return
  
  raw_sacct_data = json.loads(result.stdout.strip())
  sacct_data = {item.get("job_id"): item for item in raw_sacct_data.get("jobs")}
  
  ip_info = IpInfo()
  
  for job in jobs:
    job_sacct = sacct_data.get(job.job_id)
    
    #print(json.dumps(job_sacct)) #, indent=2))
    
    start_time = datetime.fromtimestamp(job_sacct.get("time").get("start"))
    end_time = datetime.fromtimestamp(job_sacct.get("time").get("end"))
    
    start_time = start_time.replace(tzinfo=timezone.utc)
    end_time = end_time.replace(tzinfo=timezone.utc)

    duration = (end_time - start_time).total_seconds() / 3600
        
    cpu_tres = next((item for item in job_sacct.get("tres").get("allocated") if item.get("type") == "cpu"), None)
    if cpu_tres is None:
      print(f"Failed to read CPU allocation for job with id '{job.job_id}'")
      return
    
    allocated_cpu = cpu_tres.get("count")
    
    wattage = allocated_cpu * job.cpu_profile.tdp_per_core
    
    buffer = timedelta(minutes=30)
    forecast_start = start_time - buffer
    forecast_end = end_time + buffer

    forecast = CarbonDioxideForecast(forecast_start, forecast_end, ip_info.postal)
    
    emissions = 0.0 # kg of CO2
    kwh = 0.0
    
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
    
    print(f"{job.job_id} -> kwh: {kwh:.4e}, emissions: {format_grams(emissions)} of CO2")