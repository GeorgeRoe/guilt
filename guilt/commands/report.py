from guilt.data.processed_jobs import ProcessedJobsData, ProcessedJob
from typing import List
from guilt.utility.format_grams import format_grams
from guilt.utility.format_duration import format_duration
from datetime import datetime
import shutil
import plotext as plt

def print_report(jobs: List[ProcessedJob]):
  total_emissions = sum([job.emissions for job in jobs])

  generation_mix = {}
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

def report_cmd(_):
  processed_jobs_data = ProcessedJobsData()
  
  time_splits = {}
  
  for job in processed_jobs_data.jobs.values():
    key = f"{job.start.year}-{job.start.month}"
    
    if key in time_splits:
      time_splits.get(key).append(job)
    else:
      time_splits[key] = [job]
  
  columns, _ = shutil.get_terminal_size()
  
  print("=" * columns)

  for date_str, jobs in time_splits.items():
    date = datetime.strptime(date_str, "%Y-%m")

    print(f"{date.strftime('%B %Y')}")
    print("-" * columns)

    print_report(jobs)

    print("=" * columns)
    
  print("All Time")
  print("-" * columns)
  
  print_report(processed_jobs_data.jobs.values())
  
  print("=" * columns)