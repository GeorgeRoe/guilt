from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.mappers import map_to
from guilt.constants.paths import PROCESSED_JOBS_PATH
import json

class ProcessedJobsDataRepository:
  def get_default_data(self) -> ProcessedJobsData:
    return ProcessedJobsData({})
  
  def fetch_data(self) -> ProcessedJobsData:
    with PROCESSED_JOBS_PATH.open("r") as file:
      return map_to.processed_jobs_data.from_json_file_contents(json.load(file))
    
  def submit_data(self, processed_jobs_data: ProcessedJobsData) -> None:
    PROCESSED_JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with PROCESSED_JOBS_PATH.open("w") as file:
      json.dump(map_to.json_file_contents.from_processed_jobs_data(processed_jobs_data), file, indent=2)