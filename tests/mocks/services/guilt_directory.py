from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.constants import relative_file_paths
from pathlib import Path

class MockGuiltDirectoryService(GuiltDirectoryServiceInterface):
  def __init__(self, home_directory: Path) -> None:
    self._home_directory = home_directory
    
  def get_guilt_directory_path(self) -> Path:
    return self._home_directory / relative_file_paths.GUILT_DIRECTORY
  
  def get_cpu_profiles_config_path(self) -> Path:
    return self._home_directory / relative_file_paths.CPU_PROFILES_CONFIG
  
  def get_processed_jobs_data_path(self) -> Path:
    return self._home_directory / relative_file_paths.PROCESSED_JOBS_DATA
  
  def get_unprocessed_jobs_data_path(self) -> Path:
    return self._home_directory / relative_file_paths.UNPROCESSED_JOBS_DATA