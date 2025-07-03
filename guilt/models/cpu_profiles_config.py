from dataclasses import dataclass
from guilt.models.cpu_profile import CpuProfile

@dataclass
class CpuProfilesConfig:
  default: CpuProfile
  profiles: dict[str, CpuProfile]