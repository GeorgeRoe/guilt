from pathlib import Path
from dataclasses import dataclass

@dataclass
class GetEntriesPasswordResult:
  username: str
  password: str
  user_id: str
  primary_group_id: str
  info: str
  home_directory: Path
  shell: Path