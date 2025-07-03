from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.mappers.unprocessed_jobs_data import MapToUnprocessedJobsData
from guilt.mappers.json_file_contents import MapToJsonFileContents
from pathlib import Path
from typing import Final
import json

class UnprocessedJobsDataRepository:
  DEFAULT_PATH: Final[Path] = Path.home() / ".guilt" / "unprocessed_jobs.json"
  
  def get_default_data(self) -> UnprocessedJobsData:
    return UnprocessedJobsData({})
  
  def fetch_data(self) -> UnprocessedJobsData:
    with self.DEFAULT_PATH.open("r") as file:
      return MapToUnprocessedJobsData.from_json_file_contents(json.load(file))
    
  def submit_data(self, unprocessed_jobs_data: UnprocessedJobsData):
    self.DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with self.DEFAULT_PATH.open("w") as file:
      json.dump(MapToJsonFileContents.from_unprocessed_jobs_data(unprocessed_jobs_data), file, indent=2)