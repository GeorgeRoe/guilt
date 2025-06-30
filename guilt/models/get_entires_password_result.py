from pathlib import Path

class GetEntriesPasswordResult:
  def __init__(
    self,
    username: str,
    password: str,
    user_id: str,
    primary_group_id: str,
    info: str,
    home_directory: Path,
    shell: Path
  ) -> None:
    self.username = username
    self.password = password
    self.user_id = user_id
    self.primary_group_id = primary_group_id
    self.info = info
    self.home_directory = home_directory
    self.shell = shell