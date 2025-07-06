from abc import ABC, abstractmethod
from guilt.models.processed_jobs_data import ProcessedJobsData

class ProcessedJobsDataServiceInterface(ABC):
  @abstractmethod
  def read_from_file(self) -> ProcessedJobsData:
    pass
  
  @abstractmethod
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    pass