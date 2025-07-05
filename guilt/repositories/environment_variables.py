import os
from typing import Union

class EnvironmentVariablesRepository:
  def fetch_data(self, variable_name: str) -> Union[str, None]:
    return os.getenv(variable_name)
  
  def get_current_user(self) -> Union[str, None]:
    return self.fetch_data("USER")