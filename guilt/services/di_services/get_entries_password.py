from guilt.interfaces.services.get_entries_password import GetEntriesPasswordServiceInterface
from guilt.models.get_entires_password_result import GetEntriesPasswordResult
from guilt.mappers import map_to
import subprocess

class GetEntriesPasswordService(GetEntriesPasswordServiceInterface):
  def get_entries(self) -> list[GetEntriesPasswordResult]:
    command = ["getent", "passwd"]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    return [map_to.get_entries_password_result.from_line(line) for line in result.stdout.splitlines()]