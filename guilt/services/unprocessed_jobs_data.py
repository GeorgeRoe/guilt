from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.mappers import map_to
from guilt.types.json import Json
from guilt.utility import guilt_user_file_paths 
from typing import cast
import json

class UnprocessedJobsDataService(UnprocessedJobsDataServiceInterface):
  def __init__(
    self,
    user_service: UserServiceInterface
  ) -> None:
    self.user_service = user_service
  
  def read_from_file(self) -> UnprocessedJobsData:
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot read CPU profiles config.")

    with guilt_user_file_paths.get_unprocessed_jobs_data_path(current_user).open('r') as file:
      return map_to.unprocessed_jobs_data.from_json(
        cast(Json, json.load(file))
      )
  
  def write_to_file(self, unprocessed_jobs_data: UnprocessedJobsData) -> None:
    current_user = self.user_service.get_current_user()

    if not current_user:
      raise ValueError("No user is currently logged in. Cannot write CPU profiles config.")

    path = guilt_user_file_paths.get_unprocessed_jobs_data_path(current_user)
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as file:
      json.dump(
        map_to.json.from_unprocessed_jobs_data(unprocessed_jobs_data),
        file,
        indent=2
      )