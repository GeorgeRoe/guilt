from pathlib import Path
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry
from guilt.mappers import map_to
from datetime import datetime, timedelta, timezone
from dataclasses import replace
from typing import Optional
from guilt.utility.time_series_data import WindowWithLowestSumResult
from guilt.utility.format_duration import format_duration

def execute(services: ServiceRegistry, args: Namespace):
  path = Path(args.input)
  logger.info(f"Processing batch input file: {path}")

  content = services.file_system.read_from_file(path).splitlines()

  guilt_directives = map_to.guilt_script_directives.from_json_directives(
    map_to.json.from_directive_lines(content, "#GUILT"),
    services.cpu_profiles_config.read_from_file()
  )

  slurm_directives = map_to.slurm_script_directives.from_json_directives(
    map_to.json.from_directive_lines(content, "#SBATCH")
  )

  test_job = services.slurm_batch.test_job(path, None)

  earliest_possible_start_time = test_job.start_time.replace(tzinfo=timezone.utc)
  latest_forecast_time = datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=2, minutes=-30)

  start_time: Optional[datetime] = None
  if earliest_possible_start_time + slurm_directives.time > latest_forecast_time:
    print("Your job is extends into unforecasted carbon intensity data. No delays will be applied.")
  else:
    intensity_data = map_to.time_series_data.from_carbon_intensity_forecast_result(
      services.carbon_intensity_forecast.get_forecast(
        earliest_possible_start_time,
        latest_forecast_time,
        services.ip_info.get_ip_info().postal
      )
    )

    tdp = slurm_directives.tasks_per_node * slurm_directives.cpus_per_task * slurm_directives.nodes * guilt_directives.cpu_profile.tdp_per_core

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

  job_id = services.slurm_batch.submit_job(path, start_time)
  logger.info(f"Job submitted with ID {job_id}")
  
  unprocessed_jobs_data = services.unprocessed_jobs_data.read_from_file()
  if job_id in unprocessed_jobs_data.jobs.keys():
    logger.error(f"Unprocessed job with job id '{job_id}' already exists.")
    return
  
  unprocessed_jobs_data.jobs[job_id] = UnprocessedJob(
    job_id,
    guilt_directives.cpu_profile
  )
  services.unprocessed_jobs_data.write_to_file(unprocessed_jobs_data)
  logger.debug(f"Saved new unprocessed job with ID {job_id}")

  print(f"Job submitted with ID {job_id}.")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("batch")
  subparser.add_argument("input", help="Input file or argument for batch command")
  subparser.set_defaults(function=execute)