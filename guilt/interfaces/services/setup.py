from abc import ABC, abstractmethod

class SetupServiceInterface(ABC):
  @abstractmethod
  def setup_cpu_profiles_config_file(self) -> bool:
    pass
  
  @abstractmethod
  def setup_processed_jobs_data_file(self) -> bool:
    pass
  
  @abstractmethod
  def setup_unprocessed_jobs_data_file(self) -> bool:
    pass
  
  @abstractmethod
  def setup_all_files(self) -> bool:
    pass