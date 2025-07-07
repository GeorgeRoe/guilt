from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.constants.paths import PROCESSED_JOBS_PATH
from guilt.mappers import map_to

class ProcessedJobsDataService(ProcessedJobsDataServiceInterface):
  def __init__(
    self,
    file_system_service: FileSystemServiceInterface
  ) -> None:
    self.file_system_service = file_system_service
  
  def read_from_file(self) -> ProcessedJobsData:
    return map_to.processed_jobs_data.from_json(
      self.file_system_service.read_from_json_file(PROCESSED_JOBS_PATH)
    )
  
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    self.file_system_service.write_to_json_file(
      PROCESSED_JOBS_PATH,
      map_to.json.from_processed_jobs_data(processed_jobs_data)
    )