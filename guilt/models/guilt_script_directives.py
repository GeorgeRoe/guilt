from dataclasses import dataclass
from guilt.models.cpu_profile import CpuProfile

@dataclass
class GuiltScriptDirectives:
  cpu_profile: CpuProfile