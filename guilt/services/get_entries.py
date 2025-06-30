import subprocess
from pathlib import Path
from guilt.models.get_entires_password_result import GetEntriesPasswordResult

class GetEntriesService:
  @classmethod
  def password(cls) -> list[GetEntriesPasswordResult]:
    command = ["getent", "passwd"]
      
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    get_entries_password_results: list[GetEntriesPasswordResult] = []
    for line in result.stdout.splitlines():
      parts = line.strip().split(":")
      
      if len(parts) != 7:
        raise ValueError(f"Invalid line (expected 7 fields): {line}")
      
      get_entries_password_results.append(GetEntriesPasswordResult(
        parts[0],
        parts[1],
        parts[2],
        parts[3],
        parts[4],
        Path(parts[5]),
        Path(parts[6])
      ))
      
    return get_entries_password_results