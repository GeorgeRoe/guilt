from pathlib import Path
from typing import Final

GUILT_DIRECTORY: Final[Path] = Path(".guilt")
PROCESSED_JOBS_DATA = GUILT_DIRECTORY / "processed_jobs_data.json"
UNPROCESSED_JOBS_DATA = GUILT_DIRECTORY / "unprocessed_jobs_data.json"
CPU_PROFILES_CONFIG = GUILT_DIRECTORY / "cpu_profiles_config.json"