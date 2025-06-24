import subprocess

class GetEntriesPasswdResult:
  def __init__(self, username, password, user_id, primary_group_id, info, home_directory, shell):
    self.username = username
    self.password = password
    self.user_id = user_id
    self.primary_group_id = primary_group_id
    self.info = info
    self.home_directory = home_directory
    self.shell = shell
    
  @classmethod
  def fromLine(cls, line):
    parts = line.strip().split(":")
    
    if len(parts) != 7:
      raise ValueError(f"Invalid line (expected 7 fields): {line}")
    
    parts[2] = int(parts[2])
    parts[3] = int(parts[3])
    
    return cls(*parts)

class GetEntriesService:
  @classmethod
  def passwd(cls):
    command = ["getent", "passwd"]
      
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    
    return [GetEntriesPasswdResult.fromLine(line) for line in result.stdout.splitlines()]