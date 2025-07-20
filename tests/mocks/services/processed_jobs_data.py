from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
import copy

class MockProcessedJobsDataService(ProcessedJobsDataServiceInterface):
  def __init__(self, file_contents: ProcessedJobsData = ProcessedJobsData({}), fail: bool = False) -> None:
    self._file = copy.deepcopy(file_contents)
    self._fail = fail
    
  def read_from_file(self) -> ProcessedJobsData:
    if self._fail: raise Exception("Failed to read from file")
    return self._file
  
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    if self._fail: raise Exception("Failed to write to file")
    self._file = processed_jobs_data