from guilt.interfaces.models.user import UserInterface
from guilt.utility import guilt_user_file_paths

def has_guilt_installed(user: UserInterface) -> bool:
  guilt_path = guilt_user_file_paths.get_guilt_directory_path(user)

  return guilt_path.exists() and guilt_path.is_dir()