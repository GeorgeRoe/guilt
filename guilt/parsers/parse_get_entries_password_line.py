from enum import Enum
from pathlib import Path

class _GetEntriesPasswordLineField(Enum):
  USERNAME = 0
  PASSWORD = 1
  USER_ID = 2
  PRIMARY_GROUP_ID = 3
  INFO = 4
  HOME_DIRECTORY = 5
  SHELL = 6

def _get_part_from_line(line_parts: list[str], field: _GetEntriesPasswordLineField) -> str:
  index = field.value
  if index >= len(line_parts):
    raise ValueError(f"Missing expected field at index {index}: {field.name}")
  return line_parts[index]

def get_username(line_parts: list[str]) -> str:
  return _get_part_from_line(line_parts, _GetEntriesPasswordLineField.USERNAME)

def get_password(line_parts: list[str]) -> str:
  return _get_part_from_line(line_parts, _GetEntriesPasswordLineField.PASSWORD)

def get_user_id(line_parts: list[str]) -> str:
  return _get_part_from_line(line_parts, _GetEntriesPasswordLineField.USER_ID)

def get_primary_group_id(line_parts: list[str]) -> str:
  return _get_part_from_line(line_parts, _GetEntriesPasswordLineField.PRIMARY_GROUP_ID)

def get_info(line_parts: list[str]) -> str:
  return _get_part_from_line(line_parts, _GetEntriesPasswordLineField.INFO) 

def get_home_directory(line_parts: list[str]) -> Path:
  return Path(_get_part_from_line(line_parts, _GetEntriesPasswordLineField.HOME_DIRECTORY))

def get_shell(line_parts: list[str]) -> Path:
  return Path(_get_part_from_line(line_parts, _GetEntriesPasswordLineField.SHELL))