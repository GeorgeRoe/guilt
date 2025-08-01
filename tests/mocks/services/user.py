from guilt.interfaces.services.user import UserServiceInterface
from tests.mocks.models.user import MockUser 
from typing import Optional, Iterable

class MockUserService(UserServiceInterface):
  def __init__(self, users: Iterable[MockUser]) -> None:
    self._users = users

    self._current_user = None
    for user in self._users:
      if user.is_current:
        self._current_user = user
        break

  def get_user_by_username(self, username: str) -> Optional[MockUser]:
    for user in self._users:
      if user.username == username:
        return user
    return None
  
  def get_all_users(self) -> Iterable[MockUser]:
    return self._users
  
  def get_current_user(self) -> Optional[MockUser]:
    return self._current_user