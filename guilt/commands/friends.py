from guilt.log import logger
from pathlib import Path
from guilt.services.get_entries import GetEntriesService, GetEntriesPasswdResult
from argparse import _SubParsersAction, Namespace

def execute(args: Namespace):
 
  users = []
  try:
    users = GetEntriesService.passwd()
  except Exception as e:
    logger.error(f"Error getting users: {e}")
    return

  friends: list[GetEntriesPasswdResult] = []
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
  
def register_subparser(subparsers: _SubParsersAction):
  subparser = subparsers.add_parser("friends")
  subparser.set_defaults(function=execute)