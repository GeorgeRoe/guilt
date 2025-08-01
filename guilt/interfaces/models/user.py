from abc import ABC, abstractmethod
from pathlib import Path

class UserInterface(ABC):
  @property
  @abstractmethod
  def username(self) -> str:
    pass

  @property
  @abstractmethod
  def info(self) -> str:
    pass

  @property
  @abstractmethod
  def home_directory(self) -> Path:
    pass