from guilt.interfaces.models.user import UserInterface
from pwd import struct_passwd
from pathlib import Path

class PwdUser(UserInterface):
  def __init__(self, pwd_entry: struct_passwd) -> None:
    self._pwd_entry = pwd_entry

  @property
  def username(self) -> str:
    return self._pwd_entry.pw_name
  
  @property
  def info(self) -> str:
    return self._pwd_entry.pw_gecos
  
  @property
  def home_directory(self) -> Path:
    return Path(self._pwd_entry.pw_dir)