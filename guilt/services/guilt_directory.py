from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from pathlib import Path

class GuiltDirectoryService(GuiltDirectoryServiceInterface):
  def __init__(self, environment_variables_service: EnvironmentVariablesServiceInterface) -> None:
    self.environment_variables_service = environment_variables_service

  def get_guilt_directory_path(self) -> Path:
    return self.environment_variables_service.get_home_directory() / ".guilt"

  def get_cpu_profiles_config_path(self) -> Path:
    return self.get_guilt_directory_path() / "cpu_profiles_config.json"

  def get_processed_jobs_data_path(self) -> Path:
    return self.get_guilt_directory_path() / "processed_jobs_data.json"

  def get_unprocessed_jobs_data_path(self) -> Path:
    return self.get_guilt_directory_path() / "unprocessed_jobs_data.json"