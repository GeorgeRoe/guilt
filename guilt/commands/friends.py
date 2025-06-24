from guilt.log import logger
from pathlib import Path
from guilt.services.get_entries import GetEntriesService

def execute(_):
 
  users = []
  try:
    users = GetEntriesService.passwd()
  except Exception as e:
    logger.error(f"Error getting users: {e}")
    return

  friends = []
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
  
def register_subparser(subparsers):
  subparser = subparsers.add_parser("friends")
  subparser.set_defaults(function=execute)