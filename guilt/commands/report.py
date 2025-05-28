from guilt.data.processed_jobs import ProcessedJobsData
from guilt.utility.format_grams import format_grams
from datetime import datetime, timezone

def report_cmd(_):
  processed_jobs_data = ProcessedJobsData()
  
  total_emissions = 0
  min_date = datetime.now(timezone.utc)
  
  for job in processed_jobs_data.jobs.values():
    total_emissions += job.emissions
    
    if job.start < min_date:
      min_date = job.start
    
  print(f"You have emitted {format_grams(total_emissions)} of Carbon Dioxide since {min_date}")
  print(f"Given that the average person in the UK produces approximately 12 tonnes per year, you have accounted for {total_emissions / 12_000_000} people.")