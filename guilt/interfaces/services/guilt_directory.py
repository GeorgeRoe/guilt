from abc import ABC, abstractmethod
from pathlib import Path

class GuiltDirectoryServiceInterface(ABC):
  @abstractmethod
  def get_guilt_directory_path(self) -> Path:
    pass
  
  @abstractmethod
  def get_cpu_profiles_config_path(self) -> Path:
    pass
  
  @abstractmethod
  def get_processed_jobs_data_path(self) -> Path:
    pass
  
  @abstractmethod
  def get_unprocessed_jobs_data_path(self) -> Path:
    pass