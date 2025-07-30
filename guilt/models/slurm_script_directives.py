from dataclasses import dataclass
from datetime import timedelta

@dataclass
class SlurmScriptDirectives:
  time: timedelta
  nodes: int
  tasks_per_node: int
  cpus_per_task: int