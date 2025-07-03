from guilt.models.processed_job import ProcessedJob
from dataclasses import dataclass

@dataclass
class ProcessedJobsData:
  jobs: dict[str, ProcessedJob]