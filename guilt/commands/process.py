from guilt.models.processed_job import ProcessedJob
from guilt.utility.format_grams import format_grams
from datetime import timedelta
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry

def execute(services: ServiceRegistry, args: Namespace):
  unprocessed_jobs_data = services.unprocessed_jobs_data.read_from_file()
  processed_jobs_data = services.processed_jobs_data.read_from_file()
  
  sacct_results = []
  try:
    sacct_results = services.slurm_accounting.get_jobs_with_ids(list(unprocessed_jobs_data.jobs.keys()))
  except Exception as e:
    logger.error(f"Error getting jobs: {e}")
    return
  
  if len(sacct_results) == 0:
    print("No Jobs to process")
    return
  
  ip_info = services.ip_info.get_ip_info()
  
  for result in sacct_results:
    if not "cpu" in result.resources:
      logger.warning("Skipping job due to lack of CPU resource usage information")
      continue
    
    unprocessed_job = unprocessed_jobs_data.jobs.get(str(result.job_id))

    if unprocessed_job is None:
      logger.error(f"Unprocessed job with ID '{result.job_id}' could not be found")
      return
    
    cpu_utilisation = result.resources.get("cpu")
    if cpu_utilisation is None:
      logger.error("Unprocessed job did not contain CPU utilisation.")
      return
    
    wattage = cpu_utilisation * unprocessed_job.cpu_profile.tdp_per_core
    
    buffer = timedelta(minutes=30)
    forecast_start = result.start_time - buffer
    forecast_end = result.end_time + buffer

    forecast = services.carbon_intensity_forecast.get_forecast(forecast_start, forecast_end, ip_info.postal)
    
    emissions = 0.0 # kg of CO2
    kwh = 0.0
    
    total_mix: dict[str, float] = {}
    total_mix_seconds = 0.0
    
    for segment in forecast.segments:
      overlap_start = max(result.start_time, segment.from_time)
      overlap_end = min(result.end_time, segment.to_time)
      overlap_duration = (overlap_end - overlap_start).total_seconds()
      
      if overlap_duration > 0:
        overlap_hours = overlap_duration / 3600
        overlap_kwh = (wattage * overlap_hours) / 1000
        kwh += overlap_kwh
        emissions += overlap_kwh * segment.intensity
        
        for source, percent in segment.generation_mix.items():
          total_mix[source] = total_mix.get(source, 0) + percent * overlap_duration
        total_mix_seconds += overlap_duration
    
    average_mix = {k: v / total_mix_seconds for k, v in total_mix.items()}
    
    print(f"{result.job_id} -> energy usage: {kwh:.2e} kWh, emissions: {format_grams(emissions)} of CO2")

    processed_job = ProcessedJob(
      result.start_time,
      result.end_time,
      result.job_id,
      unprocessed_job.cpu_profile,
      kwh,
      emissions,
      average_mix
    )
    
    if processed_job.job_id in processed_jobs_data.jobs.keys():
      logger.error(f"Processed job with job id '{processed_job.job_id}' already exists")
      return
    else:
      processed_jobs_data.jobs[processed_job.job_id] = processed_job
      
    if not processed_job.job_id in unprocessed_jobs_data.jobs.keys():
      logger.error(f"Unprocessed job with job id '{processed_job.job_id}' cannot be removed as it doesn't exist")
      return
    else:
      del unprocessed_jobs_data.jobs[processed_job.job_id]
  
  services.unprocessed_jobs_data.write_to_file(unprocessed_jobs_data)
  services.processed_jobs_data.write_to_file(processed_jobs_data)

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("process")
  subparser.set_defaults(function=execute)