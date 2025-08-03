from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.utility import guilt_user_file_paths
import shutil

class TeardownCommand(CommandInterface):
  def __init__(self, user_service: UserServiceInterface) -> None:
    self._user_service = user_service

  @staticmethod
  def name() -> str:
    return "teardown"
  
  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    current_user = self._user_service.get_current_user()
    if not current_user:
      print("Error: No user is currently logged in. Please log in before setting up GUILT.")
      return

    current_users_guilt_directory = guilt_user_file_paths.get_guilt_directory_path(current_user)

    if not current_users_guilt_directory.exists():
      print("Error: GUILT has not been setup!")
      return

    print("\n\033[91mFeeling too guily?\033[0m\n")
    
    print(f"This command will permanently delete the following directory: {current_users_guilt_directory}")
    response = input("Confirm by typing the following: 'I am guilty': ")
    print(f"User response: {response}")

    if response != "I am guilty":
      print("Glad to see youre not guilty, the polar bears will thank you.")
      return
    else:
      shutil.rmtree(current_users_guilt_directory)
      print(f"{current_users_guilt_directory} was removed!")
      print("\nWaving goodbye from GUILT software.")