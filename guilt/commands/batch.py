from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.utility.time_series_data import WindowWithLowestSumResult
from guilt.utility.format_duration import format_duration
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.mappers import map_to
from guilt.utility import slurm_batch
from guilt.utility.calculate_tdp_per_core import calculate_tdp_per_core
from argparse import ArgumentParser, Namespace
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import replace

class BatchCommand(CommandInterface):
  def __init__(
    self,
    repository_factory_service: RepositoryFactoryServiceInterface,
    user_service: UserServiceInterface,
    carbon_intensity_forecast_service: CarbonIntensityForecastServiceInterface,
    ip_info_service: IpInfoServiceInterface
  ) -> None:
    self._repository_factory_service = repository_factory_service
    self._user_service = user_service
    self._carbon_intensity_forecast_service = carbon_intensity_forecast_service
    self._ip_info_service = ip_info_service

  @staticmethod
  def name() -> str:
    return "batch"

  @staticmethod
  def configure_subparser(subparser: ArgumentParser) -> None:
    subparser.add_argument(
      "input",
      help="Input file or argument for batch command"
    )

  def execute(self, args: Namespace) -> None:
    path = Path(args.input)

    with path.open("r") as file:
      content = file.read().splitlines()

    current_user = self._user_service.get_current_user()

    if current_user is None:
      raise RuntimeError("No user is currently logged in. Please log in to continue.")

    guilt_directives = map_to.guilt_script_directives.from_json_directives(
      map_to.json.from_directive_lines(content, "#GUILT"),
      self._repository_factory_service.get_cpu_profiles_repository(current_user)
    )

    slurm_directives = map_to.slurm_script_directives.from_json_directives(
      map_to.json.from_directive_lines(content, "#SBATCH")
    )

    test_job = slurm_batch.test(path, None)
    test_job

    earliest_possible_start_time = test_job.start_time
    latest_forecast_time = datetime.now() + timedelta(days=2, minutes=-30)

    start_time: Optional[datetime] = None
    if earliest_possible_start_time + slurm_directives.time > latest_forecast_time:
      print("Your job is extends into unforecasted carbon intensity data. No delays will be applied.")
    else:
      intensity_data = map_to.time_series_data.from_carbon_intensity_forecast_result(
        self._carbon_intensity_forecast_service.get_forecast(
          earliest_possible_start_time,
          latest_forecast_time,
          self._ip_info_service.get_ip_info().postal
        )
      )

      tdp = slurm_directives.tasks_per_node * slurm_directives.cpus_per_task * slurm_directives.nodes * calculate_tdp_per_core(guilt_directives.cpu_profile)

      earliest_possible_time_sum = intensity_data.get_window_sum(
        earliest_possible_start_time,
        earliest_possible_start_time + slurm_directives.time
      )
      earliest_possible_time_grams = (tdp / 1000) * (earliest_possible_time_sum / 3600)

      best_times = intensity_data.get_windows_with_lowest_sum(
        earliest_possible_start_time,
        intensity_data.get_last_time() - slurm_directives.time - timedelta(minutes=1),
        slurm_directives.time,
        timedelta(minutes=1) 
      )

      best_times_with_grams: list[WindowWithLowestSumResult] = []
      for best_time in best_times:
        emissions = (tdp / 1000) * (best_time.sum_value / 3600)
        if emissions > earliest_possible_time_grams:
          continue

        emissions_saved = earliest_possible_time_grams - emissions

        delay = best_time.start_time - earliest_possible_start_time
        delay_seconds = delay.total_seconds() or 1

        if emissions_saved / delay_seconds > 0.001:
          best_times_with_grams.append(replace(best_time, sum_value=emissions))

      if not best_times_with_grams:
        print("No suitable alternative start times for the job could be found. No delays will be applied.")
      else:
        start_time = best_times_with_grams[0].start_time

        delay_seconds = (start_time - earliest_possible_start_time).total_seconds()

        print(f"If you had used 'sbatch', the job would have begun at {earliest_possible_start_time.strftime('%Y-%m-%d %H:%M')} and emitted {earliest_possible_time_grams:.2f} grams of CO2.")
        print(f"By delaying the job to {best_times_with_grams[0].start_time.strftime('%Y-%m-%d %H:%M')}, it will emit {best_times_with_grams[0].sum_value:.2f} grams of CO2.")
        print(f"You are saving {earliest_possible_time_grams- best_times_with_grams[0].sum_value:.2f} grams of CO2 by delaying the job by {format_duration(delay_seconds)}.")

    job_id = slurm_batch.submit(path, start_time)
    
    unprocessed_jobs_repository = self._repository_factory_service.get_unprocessed_jobs_repository(current_user)

    if job_id in [job.job_id for job in unprocessed_jobs_repository.get_all()]:
      print(f"Unprocessed job with ID {job_id} already exists.")
      return
    
    unprocessed_jobs_repository.upsert(UnprocessedJob(
      job_id,
      guilt_directives.cpu_profile
    ))

    unprocessed_jobs_repository.save()

    print(f"Job submitted with ID {job_id}.")