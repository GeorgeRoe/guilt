from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from typing import Union
from pathlib import Path

class MockEnvironmentVariablesService(EnvironmentVariablesServiceInterface):
  def __init__(self, variables: dict[str, str]) -> None:
    self._variables = variables
    
  def get_variable(self, name: str) -> Union[str, None]:
    return self._variables.get(name)
    
  def ensure_get_variable(self, name: str) -> str:
    variable = self.get_variable(name)
    
    if variable is None:
      raise ValueError(f"The environment variable '{name}' must be set.")
    
    return variable
  
  def get_user(self) -> str:
    return self.ensure_get_variable("USER")
  
  def get_home_directory(self) -> Path:
    home = self.get_variable("HOME")
    if home:
      return Path(home).expanduser().resolve()

    raise ValueError("The HOME environment variable must be set.")