from dataclasses import dataclass
from guilt.interfaces.models.cpu_profile import CpuProfileInterface

@dataclass
class GuiltScriptDirectives:
  cpu_profile: CpuProfileInterface