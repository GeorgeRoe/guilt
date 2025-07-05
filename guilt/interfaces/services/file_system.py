from abc import ABC, abstractmethod
from pathlib import Path

class FileSystemServiceInterface(ABC):
  @abstractmethod
  def does_path_exist(self, path: Path) -> bool:
    pass
  
  @abstractmethod
  def create_directory(self, path: Path) -> None:
    pass
  
  @abstractmethod
  def write_to_file(self, path: Path, contents: str) -> None:
    pass
  
  @abstractmethod
  def read_from_file(self, path: Path) -> str:
    pass