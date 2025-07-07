from abc import ABC, abstractmethod
from typing import Union

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