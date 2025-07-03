from dataclasses import dataclass
from datetime import datetime
from guilt.models.cpu_profile import CpuProfile

@dataclass
class ProcessedJob:
  start: datetime
  end: datetime
  job_id: str
  cpu_profile: CpuProfile
  energy: float
  emissions: float
  generation_mix: dict[str, float]