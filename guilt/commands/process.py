from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.models.processed_job import ProcessedJob
from guilt.utility.format_grams import format_grams
from datetime import timedelta

class ProcessCommand(CommandInterface):
  def __init__(
    self,
    unprocessed_jobs_data_service: UnprocessedJobsDataServiceInterface,
    processed_jobs_data_service: ProcessedJobsDataServiceInterface,
    slurm_accounting_service: SlurmAccountingServiceInterface,
    ip_info_service: IpInfoServiceInterface,
    carbon_intensity_forecast_service: CarbonIntensityForecastServiceInterface
  ) -> None:
    self._unprocessed_jobs_data_service = unprocessed_jobs_data_service
    self._processed_jobs_data_service = processed_jobs_data_service
    self._slurm_accounting_service = slurm_accounting_service
    self._ip_info_service = ip_info_service
    self._carbon_intensity_forecast_service = carbon_intensity_forecast_service

  @staticmethod
  def name() -> str:
    return "process"
  
  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    unprocessed_jobs_data = self._unprocessed_jobs_data_service.read_from_file()
    processed_jobs_data = self._processed_jobs_data_service.read_from_file()
    
    sacct_results = []
    try:
      sacct_results = self._slurm_accounting_service.get_jobs_with_ids(list(unprocessed_jobs_data.jobs.keys()))
    except Exception as e:
      print(f"Error getting jobs: {e}")
      return
    
    if len(sacct_results) == 0:
      print("No Jobs to process")
      return
    
    postal = self._ip_info_service.get_ip_info().postal
    
    for result in sacct_results:
      if not "cpu" in result.resources:
        print("Skipping job due to lack of CPU resource usage information")
        continue
      
      unprocessed_job = unprocessed_jobs_data.jobs.get(str(result.job_id))

      if unprocessed_job is None:
        print(f"Unprocessed job with ID '{result.job_id}' could not be found")
        return
      
      cpu_utilisation = result.resources.get("cpu")
      if cpu_utilisation is None:
        print("Unprocessed job did not contain CPU utilisation.")
        return
      
      wattage = cpu_utilisation * unprocessed_job.cpu_profile.tdp_per_core
      
      buffer = timedelta(minutes=30)
      forecast_start = result.start_time - buffer
      forecast_end = result.end_time + buffer

      forecast = self._carbon_intensity_forecast_service.get_forecast(forecast_start, forecast_end, postal)
      
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
        print(f"Processed job with job id '{processed_job.job_id}' already exists")
        return
      else:
        processed_jobs_data.jobs[processed_job.job_id] = processed_job
        
      if not processed_job.job_id in unprocessed_jobs_data.jobs.keys():
        print(f"Unprocessed job with job id '{processed_job.job_id}' cannot be removed as it doesn't exist")
        return
      else:
        del unprocessed_jobs_data.jobs[processed_job.job_id]
    
    self._unprocessed_jobs_data_service.write_to_file(unprocessed_jobs_data)
    self._processed_jobs_data_service.write_to_file(processed_jobs_data)