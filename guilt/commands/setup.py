from pathlib import Path
from guilt.constants import LOGO, CENTERED_TAGLINE
from guilt.data.processed_jobs import ProcessedJobsData
from guilt.data.unprocessed_jobs import UnprocessedJobsData
from guilt.config.cpu_profiles import CpuProfilesConfig

def setup_cmd(_):
  guilt_dir = Path.home() / ".guilt"

  if guilt_dir.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  CpuProfilesConfig.get_default().save()
  ProcessedJobsData().save()
  UnprocessedJobsData().save()
  
  print("GUILT is now setup!")