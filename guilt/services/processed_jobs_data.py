from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.mappers import map_to

class ProcessedJobsDataService(ProcessedJobsDataServiceInterface):
  def __init__(
    self,
    file_system_service: FileSystemServiceInterface,
    guilt_directory_service: GuiltDirectoryServiceInterface
  ) -> None:
    self.file_system_service = file_system_service
    self.guilt_directory_service = guilt_directory_service
  
  def read_from_file(self) -> ProcessedJobsData:
    return map_to.processed_jobs_data.from_json(
      self.file_system_service.read_from_json_file(self.guilt_directory_service.get_processed_jobs_data_path())
    )
  
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    self.file_system_service.write_to_json_file(
      self.guilt_directory_service.get_processed_jobs_data_path(),
      map_to.json.from_processed_jobs_data(processed_jobs_data)
    )