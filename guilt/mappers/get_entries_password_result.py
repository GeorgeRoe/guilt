from guilt.models.get_entires_password_result import GetEntriesPasswordResult
from pathlib import Path

class MapToGetEntriesPasswordResult:
  @staticmethod
  def from_line(line: str) -> GetEntriesPasswordResult:
    parts = line.strip().split(":")
    
    if len(parts) != 7:
      raise ValueError(f"Invalid line (expected 7 fields): {line}")
    
    return GetEntriesPasswordResult(
      parts[0],
      parts[1],
      parts[2],
      parts[3],
      parts[4],
      Path(parts[5]),
      Path(parts[6])
    )