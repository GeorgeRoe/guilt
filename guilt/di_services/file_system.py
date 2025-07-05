from guilt.interfaces.services.file_system import FileSystemServiceInterface
from pathlib import Path

class FileSystemService(FileSystemServiceInterface):
  def does_path_exist(self, path: Path) -> bool:
    return path.exists()
  
  def create_directory(self, path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
  
  def write_to_file(self, path: Path, contents: str) -> None:
    with path.open("w") as file:
      file.write(contents)
  
  def read_from_file(self, path: Path) -> str:
    with path.open("r") as file:
      return file.read()