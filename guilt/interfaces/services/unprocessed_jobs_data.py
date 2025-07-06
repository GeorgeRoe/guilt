from abc import ABC, abstractmethod
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData

class UnprocessedJobsDataServiceInterface(ABC):
  @abstractmethod
  def read_from_file(self) -> UnprocessedJobsData:
    pass
  
  @abstractmethod
  def write_to_file(self, unprocessed_jobs_data: UnprocessedJobsData) -> None:
    pass