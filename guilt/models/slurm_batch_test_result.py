from dataclasses import dataclass
from datetime import datetime

@dataclass
class SlurmBatchTestResult:
  job_id: str
  start_time: datetime
  processor_count: int
  nodes: str
  partition: str