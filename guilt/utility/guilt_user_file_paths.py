from guilt.interfaces.models.user import UserInterface
from guilt.constants import relative_file_paths
from pathlib import Path

def get_guilt_directory_path(user: UserInterface) -> Path:
  return user.home_directory / relative_file_paths.GUILT_DIRECTORY

def get_cpu_profiles_config_path(user: UserInterface) -> Path:
  return user.home_directory / relative_file_paths.CPU_PROFILES_CONFIG

def get_processed_jobs_data_path(user: UserInterface) -> Path:
  return user.home_directory / relative_file_paths.PROCESSED_JOBS_DATA

def get_unprocessed_jobs_data_path(user: UserInterface) -> Path:
  return user.home_directory / relative_file_paths.UNPROCESSED_JOBS_DATA