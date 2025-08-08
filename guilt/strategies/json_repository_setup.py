from guilt.interfaces.strategies.repository_setup import RepositorySetupStrategyInterface
from guilt.interfaces.models.user import UserInterface
from guilt.constants import json_repository_paths
from guilt.utility.guilt_directory import get_guilt_directory_path_for_user
from pathlib import Path
import json

class JsonRepositorySetupStrategy(RepositorySetupStrategyInterface):
  def execute(self, user: UserInterface) -> bool:
    try:
      guilt_directory = get_guilt_directory_path_for_user(user)

      json_data_path = guilt_directory / json_repository_paths.JSON_DATA_DIRECTORY

      json_data_path.mkdir(parents=True)

      empty_list_paths: list[Path] = [
        json_data_path / path
        for path in [
          json_repository_paths.CPU_PROFILES_FILE,
          json_repository_paths.PROCESSED_JOBS_FILE,
          json_repository_paths.UNPROCESSED_JOBS_FILE,
        ]
      ]
      for path in empty_list_paths:
        with path.open("w") as file:
          json.dump([], file, indent=2)

      with (json_data_path / json_repository_paths.SETTINGS_FILE).open("w") as file:
        json.dump({
          "default_cpu_profile": None
        }, file, indent=2)

      return True
    except Exception as e:
      return False