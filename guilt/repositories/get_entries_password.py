import subprocess
from guilt.models.get_entires_password_result import GetEntriesPasswordResult
from guilt.mappers.get_entries_password_result import MapToGetEntriesPasswordResult

class GetEntriesPasswordRepository: 
  @staticmethod
  def fetch_data() -> list[GetEntriesPasswordResult]:
    command = ["getent", "passwd"]
      
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    return [MapToGetEntriesPasswordResult.from_command_line(line) for line in result.stdout.splitlines()]