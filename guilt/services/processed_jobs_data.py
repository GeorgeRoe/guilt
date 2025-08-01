from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.mappers import map_to
from guilt.types.json import Json
from typing import cast
import json

class ProcessedJobsDataService(ProcessedJobsDataServiceInterface):
  def __init__(
    self,
    guilt_directory_service: GuiltDirectoryServiceInterface
  ) -> None:
    self.guilt_directory_service = guilt_directory_service
  
  def read_from_file(self) -> ProcessedJobsData:
    with self.guilt_directory_service.get_processed_jobs_data_path().open('r') as file:
      return map_to.processed_jobs_data.from_json(
        cast(Json, json.load(file))
      )
  
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    path = self.guilt_directory_service.get_processed_jobs_data_path()
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_processed_jobs_data(processed_jobs_data),
        file,
        indent=2
      )