from guilt.log import logger
from pathlib import Path
from guilt.models.lazy_get_entries_password_result import LazyGetEntriesPasswordResult
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry

def execute(services: ServiceRegistry, args: Namespace):
  users = []
  try:
    users = services.get_entries_password.get_entries()
  except Exception as e:
    logger.error(f"Error getting users: {e}")
    return

  friends: list[LazyGetEntriesPasswordResult] = []
  for user in users:
    path = user.home_directory / ".guilt"
    
    try:
      if services.file_system.does_path_exist(path):
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