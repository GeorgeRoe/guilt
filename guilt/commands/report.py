from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.interfaces.models.processed_job import ProcessedJobInterface
from guilt.utility.format_duration import format_duration
from guilt.utility.format_grams import format_grams
from guilt.utility.plotting_context import PlottingContext
from guilt.utility.calculate_tdp_per_core import calculate_tdp_per_core
from argparse import ArgumentParser, Namespace
from typing import Sequence, MutableSequence
from datetime import datetime
import shutil

class ReportCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    repository_factory_service: RepositoryFactoryServiceInterface,
    plotting_service: PlottingServiceInterface
  ) -> None:
    self._user_service = user_service
    self._repository_factory_service = repository_factory_service
    self._plotting_service = plotting_service

  @staticmethod
  def name() -> str:
    return "report"

  @staticmethod
  def configure_subparser(subparser: ArgumentParser) -> None:
    subparser.add_argument(
      "--group-by",
      help="How the report should be grouped by",
      choices=["day", "week", "month", "year"],
      default="month"
    )

  def _print_report(self, jobs: Sequence[ProcessedJobInterface]) -> None:
    total_emissions = sum([job.emissions for job in jobs])

    generation_mix: dict[str, float] = {}
    total_duration = float(0)

    for job in jobs:
      duration = (job.end - job.start).total_seconds()
      total_duration += duration
      
      for key, value in job.generation_mix.items():
        if not key in generation_mix:
          generation_mix[key] = 0
        
        generation_mix[key] += value * duration

    generation_mix = {k:v / total_duration for k, v in generation_mix.items() if v != 0}

    cpu_time = sum([(job.energy * 1000 * 3600) / calculate_tdp_per_core(job.cpu_profile) for job in jobs])
    formatted_cpu_time = format_duration(cpu_time)
    
    print(f"You ran {len(jobs)} job{'' if len(jobs) == 1 else 's'}.")
    print(f"Your total CPU time was: {formatted_cpu_time if formatted_cpu_time != '0 seconds' else 'less than 1 second'}")
    print(f"You emitted {format_grams(total_emissions)} of Carbon Dioxide.")
    
    with PlottingContext(self._plotting_service) as plot:
      plot.plot_horizontal_bar_data(
        generation_mix,
        title="Generation Mix"
      )

  def execute(self, args: Namespace) -> None:
    current_user = self._user_service.get_current_user()

    if current_user is None:
      print("You need to be logged in to generate a report.")
      return

    processed_jobs_repository = self._repository_factory_service.get_processed_jobs_repository(current_user)
    
    group_by_key_format: dict[str, str] = {
      "day": "%Y-%m-%d",
      "week": "%G-%V",
      "month": "%Y-%m",
      "year": "%Y"
    }
    
    time_splits: dict[str, MutableSequence[ProcessedJobInterface]] = {}
    for job in processed_jobs_repository.get_all():
      key = job.start.strftime(str(group_by_key_format.get(args.group_by)))
      
      if key in time_splits:
        splits_for_key = time_splits.get(key)
        if not splits_for_key is None: splits_for_key.append(job)
      else:
        time_splits[key] = [job]
    
    columns, _ = shutil.get_terminal_size()
    
    print("=" * columns)

    group_by_title_format = {
      "day": "%A %-d %B %Y",
      "week": "Week %V (%B), %G  ",
      "month": "%B %Y",
      "year": "%Y"
    }

    for date_str, jobs in time_splits.items():
      if args.group_by == "week":
        year, week = map(int, date_str.split("-"))
        date = datetime.fromisocalendar(year, week, 1)
      else:
        date = datetime.strptime(date_str, str(group_by_key_format.get(args.group_by)))

      print(f"{date.strftime(str(group_by_title_format.get(args.group_by)))}")
      print("-" * columns)

      self._print_report(jobs)

      print("=" * columns)
      
    print("All Time")
    print("-" * columns)
    
    self._print_report(processed_jobs_repository.get_all())
    
    print("=" * columns)