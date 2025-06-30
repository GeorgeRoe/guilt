from datetime import datetime
from dataclasses import dataclass

@dataclass
class SlurmAccountingResult:
  job_id: str
  start_time: datetime
  end_time: datetime
  resources: dict[str, float]