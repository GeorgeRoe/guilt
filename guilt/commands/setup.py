from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.strategies.repository_setup import RepositorySetupStrategyInterface
from guilt.utility.guilt_directory import create_guilt_directory_for_user, does_user_have_guilt_directory
from guilt.constants import branding

class SetupCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    repository_setup_strategy: RepositorySetupStrategyInterface
  ) -> None:
    self._user_service = user_service
    self._repository_setup_strategy = repository_setup_strategy

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

    if does_user_have_guilt_directory(current_user):
      print("Error: GUILT has already been setup!")
      return

    print("\n\033[91m" + branding.LOGO + "\n" * 2 + branding.CENTERED_TAGLINE)
    print("\033[0m")

    create_guilt_directory_for_user(current_user)
    self._repository_setup_strategy.execute(current_user)

    print("GUILT is now setup!")