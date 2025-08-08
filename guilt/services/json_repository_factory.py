from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.repositories.json_cpu_profiles import JsonCpuProfilesRepository
from guilt.repositories.json_processed_jobs import JsonProcessedJobsRepository
from guilt.repositories.json_unprocessed_jobs import JsonUnprocessedJobsRepository
from guilt.repositories.json_settings import JsonSettingsRepository
from guilt.interfaces.models.user import UserInterface
from guilt.utility.guilt_directory import get_guilt_directory_path_for_user
from guilt.constants import json_repository_paths
from pathlib import Path
from enum import Enum

class JsonRepositoryFactoryService(RepositoryFactoryServiceInterface):
  def __init__(self) -> None:
    self._cpu_profile_repositories: dict[Path, JsonCpuProfilesRepository] = {}

  def get_cpu_profiles_repository(self, user: UserInterface) -> JsonCpuProfilesRepository:
    if user.home_directory not in self._cpu_profile_repositories:
      self._cpu_profile_repositories[user.home_directory] = JsonCpuProfilesRepository(
        get_guilt_directory_path_for_user(user) / json_repository_paths.JSON_DATA_DIRECTORY / json_repository_paths.CPU_PROFILES_FILE
      )
    return self._cpu_profile_repositories[user.home_directory]

  def get_processed_jobs_repository(self, user: UserInterface) -> JsonProcessedJobsRepository:
    return JsonProcessedJobsRepository(
      get_guilt_directory_path_for_user(user) / json_repository_paths.JSON_DATA_DIRECTORY / json_repository_paths.PROCESSED_JOBS_FILE,
      self.get_cpu_profiles_repository(user)
    )

  def get_unprocessed_jobs_repository(self, user: UserInterface) -> JsonUnprocessedJobsRepository:
    return JsonUnprocessedJobsRepository(
      get_guilt_directory_path_for_user(user) / json_repository_paths.JSON_DATA_DIRECTORY / json_repository_paths.UNPROCESSED_JOBS_FILE,
      self.get_cpu_profiles_repository(user)
    )

  def get_settings_repository(self, user: UserInterface) -> JsonSettingsRepository:
    return JsonSettingsRepository(
      get_guilt_directory_path_for_user(user) / json_repository_paths.JSON_DATA_DIRECTORY / json_repository_paths.SETTINGS_FILE,
      self.get_cpu_profiles_repository(user)
    )