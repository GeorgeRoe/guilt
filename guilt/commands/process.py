from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.models.processed_job import ProcessedJob
from guilt.utility.format_grams import format_grams
from guilt.utility import slurm_accounting
from guilt.utility.calculate_tdp_per_core import calculate_tdp_per_core
from guilt.utility import ip_info
from datetime import timedelta

class ProcessCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    repository_factory_service: RepositoryFactoryServiceInterface,
    carbon_intensity_forecast_service: CarbonIntensityForecastServiceInterface
  ) -> None:
    self._user_service = user_service
    self._repository_factory_service = repository_factory_service
    self._carbon_intensity_forecast_service = carbon_intensity_forecast_service

  @staticmethod
  def name() -> str:
    return "process"
  
  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    current_user = self._user_service.get_current_user()

    if current_user is None:
      print("No current user found. Please log in first.")
      return

    processed_jobs_repository= self._repository_factory_service.get_processed_jobs_repository(current_user)
    unprocessed_jobs_repository = self._repository_factory_service.get_unprocessed_jobs_repository(current_user)

    job_ids = [job.job_id for job in unprocessed_jobs_repository.get_all()]
    sacct_results = slurm_accounting.run(
      job_ids=job_ids
    )

    if len(sacct_results) == 0:
      print("No Jobs to process")
      return
    
    postal = ip_info.get().postal
    
    for result in sacct_results:
      if not "cpu" in result.resources:
        print("Skipping job due to lack of CPU resource usage information")
        continue
      
      unprocessed_job = unprocessed_jobs_repository.get(result.job_id)

      if unprocessed_job is None:
        print(f"Unprocessed job with ID '{result.job_id}' could not be found")
        return
      
      cpu_utilisation = result.resources.get("cpu")
      if cpu_utilisation is None:
        print("Unprocessed job did not contain CPU utilisation.")
        return
      
      wattage = cpu_utilisation * calculate_tdp_per_core(unprocessed_job.cpu_profile)
      
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

      processed_jobs_repository.upsert(processed_job)
      unprocessed_jobs_repository.delete(unprocessed_job.job_id)
    
    if unprocessed_jobs_repository.save():
      processed_jobs_repository.save()
    else:
      print("Failed to save processed jobs repository.")
      return