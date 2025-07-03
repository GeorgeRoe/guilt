from dataclasses import dataclass
from guilt.models.cpu_profile import CpuProfile

@dataclass
class UnprocessedJob:
  job_id: str
  cpu_profile: CpuProfile