from guilt.interfaces.models.user import UserInterface
from pathlib import Path
import shutil

GUILT_DIRECTORY_NAME = ".guilt"

def get_guilt_directory_path_for_user(user: UserInterface) -> Path:
  return user.home_directory / GUILT_DIRECTORY_NAME

def does_user_have_guilt_directory(user: UserInterface) -> bool:
  path = get_guilt_directory_path_for_user(user)

  try:
    return path.exists() and path.is_dir()
  except PermissionError as e:
    return False

def create_guilt_directory_for_user(user: UserInterface) -> None:
  path = get_guilt_directory_path_for_user(user)

  path.mkdir()

def remove_guilt_directory_for_user(user: UserInterface) -> None:
  path = get_guilt_directory_path_for_user(user)

  shutil.rmtree(path)