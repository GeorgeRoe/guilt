from abc import ABC, abstractmethod
from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.interfaces.repositories.processed_jobs import ProcessedJobsRepositoryInterface
from guilt.interfaces.repositories.unprocessed_jobs import UnprocessedJobsRepositoryInterface
from guilt.interfaces.repositories.settings import SettingsRepositoryInterface
from guilt.interfaces.models.user import UserInterface

class RepositoryFactoryServiceInterface(ABC):
  @abstractmethod
  def get_cpu_profiles_repository(self, user: UserInterface) -> CpuProfilesRepositoryInterface:
    pass

  @abstractmethod
  def get_unprocessed_jobs_repository(self, user: UserInterface) -> UnprocessedJobsRepositoryInterface:
    pass

  @abstractmethod
  def get_processed_jobs_repository(self, user: UserInterface) -> ProcessedJobsRepositoryInterface:
    pass

  @abstractmethod
  def get_settings_repository(self, user: UserInterface) -> SettingsRepositoryInterface:
    pass