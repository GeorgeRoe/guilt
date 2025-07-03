from pathlib import Path
from typing import Final

GUILT_DIRECTORY: Final = Path.home()

CPU_PROFILES_PATH: Final = GUILT_DIRECTORY / "cpu_profiles.json"
PROCESSED_JOBS_PATH: Final = GUILT_DIRECTORY / "processed_jobs.json"
UNPROCESSED_JOBS_PATH: Final = GUILT_DIRECTORY / "unprocessed_jobs.json"