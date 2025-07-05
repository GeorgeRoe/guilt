from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from typing import Union
import os

class EnvironmentVariablesService(EnvironmentVariablesServiceInterface):
  def get_variable(self, name: str) -> Union[str, None]:
    return os.getenv(name)
  
  def get_user(self) -> Union[str, None]:
    return self.get_variable("USER")