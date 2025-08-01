from typing import Optional
from pathlib import Path
from guilt.parsers import parse_get_entries_password_line
from guilt.interfaces.models.user import UserInterface

class LazyGetEntriesPasswordResult(UserInterface):
  def __init__(self, line: str) -> None:
    self._line_parts = line.strip().split(":")

    self._username: Optional[str] = None
    self._password: Optional[str] = None
    self._user_id: Optional[str] = None
    self._primary_group_id: Optional[str] = None
    self._info: Optional[str] = None
    self._home_directory: Optional[Path] = None
    self._shell: Optional[Path] = None
  
  @property
  def username(self) -> str:
    if self._username is None:
      self._username = parse_get_entries_password_line.get_username(self._line_parts)
    return self._username

  @property
  def password(self) -> str:
    if self._password is None:
      self._password = parse_get_entries_password_line.get_password(self._line_parts)
    return self._password
  
  @property
  def user_id(self) -> str:
    if self._user_id is None:
      self._user_id = parse_get_entries_password_line.get_user_id(self._line_parts)
    return self._user_id
  
  @property
  def primary_group_id(self) -> str:
    if self._primary_group_id is None:
      self._primary_group_id = parse_get_entries_password_line.get_primary_group_id(self._line_parts)
    return self._primary_group_id
  
  @property
  def info(self) -> str:
    if self._info is None:
      self._info = parse_get_entries_password_line.get_info(self._line_parts)
    return self._info
  
  @property
  def home_directory(self) -> Path:
    if self._home_directory is None:
      self._home_directory = parse_get_entries_password_line.get_home_directory(self._line_parts)
    return self._home_directory
  
  @property
  def shell(self) -> Path:
    if self._shell is None:
      self._shell = parse_get_entries_password_line.get_shell(self._line_parts)
    return self._shell