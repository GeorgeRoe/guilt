from abc import ABC, abstractmethod
from typing import Optional, Iterable
from guilt.interfaces.models.user import UserInterface

class UserServiceInterface(ABC):
  @abstractmethod
  def get_user_by_username(self, username: str) -> Optional[UserInterface]:
    pass

  @abstractmethod
  def get_all_users(self) -> Iterable[UserInterface]:
    pass

  @abstractmethod
  def get_current_user(self) -> Optional[UserInterface]:
    pass