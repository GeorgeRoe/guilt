from guilt.data.processed_jobs import ProcessedJobsData, ProcessedJob
from guilt.utility.format_grams import format_grams
from guilt.utility.format_duration import format_duration
from datetime import datetime
import shutil
import plotext as plt
from argparse import _SubParsersAction, ArgumentParser, Namespace # type: ignore

def print_report(jobs: list[ProcessedJob]):
  total_emissions = sum([job.emissions for job in jobs])

  generation_mix: dict[str, float] = {}
  total_duration = 0

  for job in jobs:
    duration = (job.end - job.start).total_seconds()
    total_duration += duration
    
    for key, value in job.generation_mix.items():
      if not key in generation_mix:
        generation_mix[key] = 0
      
      generation_mix[key] += value * duration

  generation_mix = {k:v / total_duration for k, v in generation_mix.items() if v != 0}

  cpu_time = sum([(job.energy * 1000 * 3600) / job.cpu_profile.tdp_per_core for job in jobs])
  formatted_cpu_time = format_duration(cpu_time)
  
  print(f"You ran {len(jobs)} job{'' if len(jobs) == 1 else 's'}.")
  print(f"Your total CPU time was: {formatted_cpu_time if formatted_cpu_time != '0 seconds' else 'less than 1 second'}")
  print(f"You emitted {format_grams(total_emissions)} of Carbon Dioxide.")
  
  columns, _ = shutil.get_terminal_size()
  
  sources = list(generation_mix.keys())
  values = [generation_mix.get(source) for source in sources]

  plt.clf()
  plt.simple_bar(sources, values, title = "Generation Mix", width = columns - 1)
  plt.show()

def execute(args: Namespace):
  processed_jobs_data = ProcessedJobsData.from_file()
  
  group_by_key_format: dict[str, str] = {
    "day": "%Y-%m-%d",
    "week": "%G-%V",
    "month": "%Y-%m",
    "year": "%Y"
  }
  
  time_splits: dict[str, list[ProcessedJob]] = {}
  for job in processed_jobs_data.jobs.values():
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

    print_report(jobs)

    print("=" * columns)
    
  print("All Time")
  print("-" * columns)
  
  print_report(list(processed_jobs_data.jobs.values()))
  
  print("=" * columns)
  
def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
  subparser = subparsers.add_parser("report")
  subparser.add_argument(
    "--group-by",
    help="How the report should be grouped by",
    choices=["day", "week", "month", "year"],
    default="month"
  )
  subparser.set_defaults(function=execute)