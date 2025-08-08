from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.models.user import UserInterface
from guilt.utility.guilt_directory import does_user_have_guilt_directory 
from typing import Sequence

class FriendsCommand(CommandInterface):
  def __init__(self, user_service: UserServiceInterface) -> None:
    self._user_service = user_service

  @staticmethod
  def name() -> str:
    return "friends"

  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    friends: Sequence[UserInterface] = [
      user
      for user
      in self._user_service.get_all_users()
      if does_user_have_guilt_directory(user)
    ]

    if len(friends) == 0:
      print("You are the only one using GUILT! :(")
      return
    
    print("Here are the other people using GUILT on this system:")
    [print(f"{friend.username} -> {friend.info}") for friend in friends]