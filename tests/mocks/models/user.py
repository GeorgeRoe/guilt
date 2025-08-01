from guilt.interfaces.models.user import UserInterface
from pathlib import Path

class MockUser(UserInterface):
  def __init__(self, username: str, info: str, home_directory: Path, is_current: bool = False) -> None:
    self._username = username
    self._info = info
    self._home_directory = home_directory
    self._is_current = is_current

  @property
  def username(self) -> str:
    return self._username
  
  @property
  def info(self) -> str:
    return self._info
  
  @property
  def home_directory(self) -> Path:
    return self._home_directory

  @property
  def is_current(self) -> bool:
    return self._is_current