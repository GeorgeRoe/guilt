from guilt.log import logger
from pathlib import Path
from guilt.models.get_entires_password_result import GetEntriesPasswordResult
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependencies.manager import dependency_manager

get_entires_password_repository = dependency_manager.repository.get_entries_password

def execute(args: Namespace):
  users = []
  try:
    users = get_entires_password_repository.fetch_data()
  except Exception as e:
    logger.error(f"Error getting users: {e}")
    return

  friends: list[GetEntriesPasswordResult] = []
  for user in users:
    path = Path(user.home_directory) / ".guilt"
    
    try:
      if path.exists():
        friends.append(user)
    except:
      logger.warning(f"Cannot access path '{path}'")
      
  if len(friends) == 0:
    print("You are the only one using GUILT! :(")
    return
  
  print("Here are the other people using GUILT on this system:")
  [print(f"{friend.username} -> {friend.info}") for friend in friends]

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("friends")
  subparser.set_defaults(function=execute)