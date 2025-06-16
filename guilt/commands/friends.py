import subprocess
from guilt.log import logger
from pathlib import Path

class User:
  def __init__(self, username: str, info: str, home_directory: str):
    self.username = username
    self.info = info
    self.home_directory = home_directory
    
  @classmethod
  def from_line(cls, line: str):
    items = line.split(":")
    return cls(items[0], items[4], items[5])
  
  def __repr__(self):
    return (
        f"User(username={self.username}, "
        f"info='{self.info}', "
        f"home_directory='{self.home_directory}')"
    )    

def execute(_):
  command = ["getent", "passwd"]
  logger.info(f"Running command: {' '.join(command)}")
  try:
    result = subprocess.run(command, capture_output=True, text=True)
  except Exception as e:
    logger.error(f"Error running command '{' '.join(command)}': {e}")
    return
  
  users = [User.from_line(line) for line in result.stdout.splitlines()]
  
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