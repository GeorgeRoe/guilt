from dataclasses import dataclass
from datetime import timedelta

@dataclass
class SlurmScriptDirectives:
  time: timedelta