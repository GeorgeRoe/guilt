from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.constants.paths import UNPROCESSED_JOBS_PATH
from guilt.mappers import map_to

class UnprocessedJobsDataService(UnprocessedJobsDataServiceInterface):
  def __init__(
    self,
    file_system_service: FileSystemServiceInterface
  ) -> None:
    self.file_system_service = file_system_service
  
  def read_from_file(self) -> UnprocessedJobsData:
    return map_to.unprocessed_jobs_data.from_json(
      self.file_system_service.read_from_json_file(UNPROCESSED_JOBS_PATH)
    )
  
  def write_to_file(self, unprocessed_jobs_data: UnprocessedJobsData) -> None:
    self.file_system_service.write_to_json_file(
      UNPROCESSED_JOBS_PATH,
      map_to.json.from_unprocessed_jobs_data(unprocessed_jobs_data)
    )