from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.utility.has_guilt_installed import has_guilt_installed
from guilt.constants import branding

class SetupCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    cpu_profiles_config_service: CpuProfilesConfigServiceInterface,
    processed_jobs_data_service: ProcessedJobsDataServiceInterface,
    unprocessed_jobs_data_service: UnprocessedJobsDataServiceInterface
  ) -> None:
    self._user_service = user_service
    self._cpu_profiles_config_service = cpu_profiles_config_service
    self._processed_jobs_data_service = processed_jobs_data_service
    self._unprocessed_jobs_data_service = unprocessed_jobs_data_service

  @staticmethod
  def name() -> str:
    return "setup"
  
  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    current_user = self._user_service.get_current_user()
    if not current_user:
      print("Error: No user is currently logged in. Please log in before setting up GUILT.")
      return

    if has_guilt_installed(current_user):
      print("Error: GUILT has already been setup!")
      return

    print("\n\033[91m" + branding.LOGO + "\n" * 2 + branding.CENTERED_TAGLINE)
    print("\033[0m")

    try:
      self._cpu_profiles_config_service.write_to_file(
        self._cpu_profiles_config_service.get_default()
      )
    except Exception as e:
      print(f"Error setting up CPU profiles config file: {e}")
      return

    try:
      self._processed_jobs_data_service.write_to_file(ProcessedJobsData({}))
    except Exception as e:
      print(f"Error setting up processed jobs data file: {e}")
      return
    
    try:
      self._unprocessed_jobs_data_service.write_to_file(UnprocessedJobsData({}))
    except Exception as e:
      print(f"Error setting up unprocessed jobs data file: {e}")
      return

    print("GUILT is now setup!")