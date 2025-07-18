from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from dataclasses import dataclass
from pathlib import Path

TESTING_GUILT_DIR: Path = Path("guilt_testing")

@dataclass
class TestGuiltDirectories:
  guilt_dir: Path = TESTING_GUILT_DIR
  cpu_profiles_config: Path = TESTING_GUILT_DIR / "cpu_profiles_config.json"
  processed_jobs_data: Path = TESTING_GUILT_DIR / "processed_jobs_data.json"
  unprocessed_jobs_data: Path = TESTING_GUILT_DIR / "unprocessed_jobs_data.json"

class MockGuiltDirectoryService(GuiltDirectoryServiceInterface):
  def __init__(self, directories: TestGuiltDirectories = TestGuiltDirectories()) -> None:
    self._directories = directories
    
  def get_guilt_directory_path(self) -> Path:
    return self._directories.guilt_dir
  
  def get_cpu_profiles_config_path(self) -> Path:
    return self._directories.cpu_profiles_config
  
  def get_processed_jobs_data_path(self) -> Path:
    return self._directories.processed_jobs_data
  
  def get_unprocessed_jobs_data_path(self) -> Path:
    return self._directories.unprocessed_jobs_data