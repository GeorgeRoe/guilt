from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.utility.guilt_directory import remove_guilt_directory_for_user, does_user_have_guilt_directory, get_guilt_directory_path_for_user

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

    if not does_user_have_guilt_directory(current_user):
      print("Error: GUILT has not been setup!")
      return

    print("\n\033[91mFeeling too guily?\033[0m\n")

    current_users_guilt_directory = get_guilt_directory_path_for_user(current_user)
    
    print(f"This command will permanently delete the following directory: {current_users_guilt_directory}")
    response = input("Confirm by typing the following: 'I am guilty': ")
    print(f"User response: {response}")

    if response != "I am guilty":
      print("Glad to see youre not guilty, the polar bears will thank you.")
      return
    else:
      remove_guilt_directory_for_user(current_user)
      print(f"{current_users_guilt_directory} was removed!")
      print("\nWaving goodbye from GUILT software.")