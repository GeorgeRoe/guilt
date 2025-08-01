from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.mappers import map_to
from guilt.types.json import Json
from typing import cast
import json

class UnprocessedJobsDataService(UnprocessedJobsDataServiceInterface):
  def __init__(
    self,
    guilt_directory_service: GuiltDirectoryServiceInterface
  ) -> None:
    self.guilt_directory_service = guilt_directory_service
  
  def read_from_file(self) -> UnprocessedJobsData:
    with self.guilt_directory_service.get_unprocessed_jobs_data_path().open('r') as file:
      return map_to.unprocessed_jobs_data.from_json(
        cast(Json, json.load(file))
      )
  
  def write_to_file(self, unprocessed_jobs_data: UnprocessedJobsData) -> None:
    path = self.guilt_directory_service.get_unprocessed_jobs_data_path()
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_unprocessed_jobs_data(unprocessed_jobs_data),
        file,
        indent=2
      )