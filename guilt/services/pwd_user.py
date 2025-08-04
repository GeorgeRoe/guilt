from guilt.interfaces.services.user import UserServiceInterface
from guilt.models.pwd_user import PwdUser
from typing import Optional, Iterable
import pwd
import os

class PwdUserService(UserServiceInterface):
  def get_user_by_username(self, username: str) -> Optional[PwdUser]:
    try:
      return PwdUser(pwd.getpwnam(username))
    except KeyError:
      return None

  def get_all_users(self) -> Iterable[PwdUser]:
    return [PwdUser(user) for user in pwd.getpwall()]

  def get_current_user(self) -> Optional[PwdUser]:
    try:
      return PwdUser(pwd.getpwuid(os.getuid()))
    except KeyError:
      return None