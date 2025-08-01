from guilt.interfaces.services.user import UserServiceInterface
from guilt.models.lazy_get_entries_password_result import LazyGetEntriesPasswordResult
from typing import Optional, Iterable
import subprocess
import getpass

class UserService(UserServiceInterface):
  def _run_command(self, username: Optional[str] = None) -> str:
    command = ["getent", "passwd"]

    if username:
      command.append(username)
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")

    return result.stdout
    
  def get_user_by_username(self, username: str) -> Optional[LazyGetEntriesPasswordResult]:
    result = self._run_command(username)
    
    return LazyGetEntriesPasswordResult(result) if result else None

  def get_all_users(self) -> Iterable[LazyGetEntriesPasswordResult]:
    return [LazyGetEntriesPasswordResult(line) for line in self._run_command().splitlines()]
  
  def get_current_user(self) -> Optional[LazyGetEntriesPasswordResult]:
    username = getpass.getuser()
    return self.get_user_by_username(username)