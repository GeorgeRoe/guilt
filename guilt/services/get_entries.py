import subprocess
from pathlib import Path

class GetEntriesPasswdResult:
  def __init__(self, username: str, password: str, user_id: str, primary_group_id: str, info: str, home_directory: Path, shell: Path) -> None:
    self.username = username
    self.password = password
    self.user_id = user_id
    self.primary_group_id = primary_group_id
    self.info = info
    self.home_directory = home_directory
    self.shell = shell
    
  @classmethod
  def fromLine(cls, line: str) -> "GetEntriesPasswdResult":
    parts = line.strip().split(":")
    
    if len(parts) != 7:
      raise ValueError(f"Invalid line (expected 7 fields): {line}")
    
    username = parts[0]
    password = parts[1]
    user_id = parts[2]
    primary_group_id = parts[3]
    info = parts[4]
    home_directory = Path(parts[5])
    shell = Path(parts[6])
    
    return cls(username, password, user_id, primary_group_id, info, home_directory, shell)

class GetEntriesService:
  @classmethod
  def passwd(cls) -> list[GetEntriesPasswdResult]:
    command = ["getent", "passwd"]
      
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    return [GetEntriesPasswdResult.fromLine(line) for line in result.stdout.splitlines()]