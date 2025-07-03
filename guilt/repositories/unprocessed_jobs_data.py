from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.mappers.unprocessed_jobs_data import MapToUnprocessedJobsData
from guilt.mappers.json_file_contents import MapToJsonFileContents
from guilt.constants.paths import UNPROCESSED_JOBS_PATH
import json

class UnprocessedJobsDataRepository:
  def get_default_data(self) -> UnprocessedJobsData:
    return UnprocessedJobsData({})
  
  def fetch_data(self) -> UnprocessedJobsData:
    with UNPROCESSED_JOBS_PATH.open("r") as file:
      return MapToUnprocessedJobsData.from_json_file_contents(json.load(file))
    
  def submit_data(self, unprocessed_jobs_data: UnprocessedJobsData):
    UNPROCESSED_JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with UNPROCESSED_JOBS_PATH.open("w") as file:
      json.dump(MapToJsonFileContents.from_unprocessed_jobs_data(unprocessed_jobs_data), file, indent=2)