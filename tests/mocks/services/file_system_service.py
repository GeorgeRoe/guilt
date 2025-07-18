from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.types.json import Json
from pathlib import Path
from typing import Union, Optional, cast
import json

FileSystemNode = Union[str, dict[str, "FileSystemNode"]]

def add_path_to_file_system(fs: FileSystemNode, path: Path, contents: Optional[str] = None) -> None:
  current = cast(dict[str, FileSystemNode], fs)

  for i, part in enumerate(path.parts):
    is_last = i == len(path.parts) - 1

    if part not in current:
      if is_last and contents is not None:
        current[part] = contents
      else:
        current[part] = {}

    elif isinstance(current[part], str) and not is_last:
      raise ValueError(f"Cannot create subpath inside file: {part}")

    if not is_last:
      current = cast(dict[str, FileSystemNode], current[part])
      
def get_node_at_path(fs: FileSystemNode, path: Path) -> FileSystemNode:
  current: FileSystemNode = fs

  for i, part in enumerate(path.parts):
    if not isinstance(current, dict):
      raise ValueError(f"Path component '{path.parts[i - 1]}' is a file, not a directory")

    if part not in current:
      raise FileNotFoundError(f"Path does not exist: {'/'.join(path.parts[:i+1])}")

    current = current[part]

  return current

class MockFileSystemService(FileSystemServiceInterface):
  def __init__(self, file_system: FileSystemNode = {}) -> None:
    self._file_system = file_system
    
  def does_path_exist(self, path: Path) -> bool:
    current = self._file_system
    
    for part in path.parts:
      if isinstance(current, str):
        return False
      
      chosen = current.get(part)
      if chosen is None:
        return False
      
      current = chosen
      
    return True
  
  def create_directory(self, path: Path) -> None:
    current = self._file_system

    for part in path.parts:
      if isinstance(current, str):
        raise NotADirectoryError(f"Cannot create subdirectory '{part}' under a file.")

      if part not in current:
        current[part] = {}

      elif isinstance(current[part], str):
        raise NotADirectoryError(f"'{part}' is a file, not a directory.")

      current = current[part]
      
  def write_to_file(self, path: Path, contents: str) -> None:
    parent = self._file_system
    for part in path.parts[:-1]:
      if isinstance(parent, str):
        raise NotADirectoryError(f"Cannot descend into file: {part}")
      parent = parent.setdefault(part, {})
    if not isinstance(parent, dict):
      raise NotADirectoryError("Final parent is not a directory.")

    parent[path.name] = contents

  def read_from_file(self, path: Path) -> str:
    current = self._file_system
    for part in path.parts:
      if not isinstance(current, dict):
        raise FileNotFoundError(f"'{part}' is not a directory.")
      chosen = current.get(part)
      if chosen is None:
        raise FileNotFoundError(f"'{part}' not found.")
      current = chosen
    if not isinstance(current, str):
      raise IsADirectoryError(f"'{path}' is a directory, not a file.")
    return current

  def write_to_json_file(self, path: Path, data: Json) -> None:
    json_str = json.dumps(data, indent=2)
    self.write_to_file(path, json_str)

  def read_from_json_file(self, path: Path) -> Json:
    raw = self.read_from_file(path)
    return cast(Json, json.loads(raw))