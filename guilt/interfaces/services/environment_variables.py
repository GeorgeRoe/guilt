from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

class EnvironmentVariablesServiceInterface(ABC):
  @abstractmethod
  def get_variable(self, name: str) -> Union[str, None]:
    pass
  
  @abstractmethod
  def ensure_get_variable(self, name: str) -> str:
    pass
  
  @abstractmethod
  def get_user(self) -> str:
    pass
  
  @abstractmethod
  def get_home_directory(self) -> Path:
    pass