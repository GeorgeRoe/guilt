from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from pathlib import Path
from guilt.constants import relative_file_paths

class GuiltDirectoryService(GuiltDirectoryServiceInterface):
  def __init__(self, environment_variables_service: EnvironmentVariablesServiceInterface) -> None:
    self.environment_variables_service = environment_variables_service

  def get_guilt_directory_path(self) -> Path:
    return self.environment_variables_service.get_home_directory() / relative_file_paths.GUILT_DIRECTORY

  def get_cpu_profiles_config_path(self) -> Path:
    return self.get_guilt_directory_path() / relative_file_paths.CPU_PROFILES_CONFIG

  def get_processed_jobs_data_path(self) -> Path:
    return self.get_guilt_directory_path() / relative_file_paths.PROCESSED_JOBS_DATA

  def get_unprocessed_jobs_data_path(self) -> Path:
    return self.get_guilt_directory_path() / relative_file_paths.UNPROCESSED_JOBS_DATA