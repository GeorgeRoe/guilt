from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.setup import SetupServiceInterface
from guilt.utility import guilt_user_file_paths
from guilt.constants import branding

class SetupCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    setup_service: SetupServiceInterface
  ) -> None:
    self._user_service = user_service
    self._setup_service = setup_service

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

    if guilt_user_file_paths.get_guilt_directory_path(current_user).exists():
      print("Error: GUILT has already been setup!")
      return

    print("\n\033[91m" + branding.LOGO + "\n" * 2 + branding.CENTERED_TAGLINE)
    print("\033[0m")

    if self._setup_service.setup_all_files():
      print("GUILT is now setup!")
    else:
      print("failed to setup GUILT.")