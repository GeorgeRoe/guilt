from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProcessedJob:
  start: datetime
  end: datetime
  job_id: str
  cpu_profile: CpuProfile
  energy: float
  emissions: float
  generation_mix: dict[str, float]