from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.mappers import map_to
from guilt.types.json import Json
from guilt.utility import guilt_user_file_paths
from typing import cast
import json

class ProcessedJobsDataService(ProcessedJobsDataServiceInterface):
  def __init__(
    self,
    user_service: UserServiceInterface
  ) -> None:
    self.user_service = user_service
  
  def read_from_file(self) -> ProcessedJobsData:
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot read CPU profiles config.")

    with guilt_user_file_paths.get_processed_jobs_data_path(current_user).open('r') as file:
      return map_to.processed_jobs_data.from_json(
        cast(Json, json.load(file))
      )
  
  def write_to_file(self, processed_jobs_data: ProcessedJobsData) -> None:
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot write CPU profiles config.")

    path = guilt_user_file_paths.get_processed_jobs_data_path(current_user)
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_processed_jobs_data(processed_jobs_data),
        file,
        indent=2
      )