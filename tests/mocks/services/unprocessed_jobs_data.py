from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
import copy

class MockUnprocessedJobsDataService(UnprocessedJobsDataServiceInterface):
  def __init__(self, file_contents: UnprocessedJobsData = UnprocessedJobsData({}), fail: bool = False) -> None:
    self._file = copy.deepcopy(file_contents)
    self._fail = fail
    
  def read_from_file(self) -> UnprocessedJobsData:
    if self._fail: raise Exception("Failed to read from file")
    return self._file
  
  def write_to_file(self, unprocessed_jobs_data: UnprocessedJobsData) -> None:
    if self._fail: raise Exception("Failed to write to file")
    self._file = unprocessed_jobs_data