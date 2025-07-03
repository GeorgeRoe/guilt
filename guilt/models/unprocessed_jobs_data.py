from guilt.models.unprocessed_job import UnprocessedJob
from dataclasses import dataclass

@dataclass
class UnprocessedJobsData:
  jobs: dict[str, UnprocessedJob]