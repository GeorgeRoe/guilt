import shutil
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry
from guilt.utility import guilt_user_file_paths

def execute(services: ServiceRegistry, args: Namespace):
  current_user = services.user.get_current_user()
  if not current_user:
    print("Error: No user is currently logged in. Please log in before setting up GUILT.")
    return

  current_users_guilt_directory = guilt_user_file_paths.get_guilt_directory_path(current_user)

  if not current_users_guilt_directory.exists():
    logger.error("Error: GUILT has not been setup!")
    return

  print("\n\033[91mFeeling too guily?\033[0m\n")
  
  print(f"This command will permanently delete the following directory: {current_users_guilt_directory}")
  response = input("Confirm by typing the following: 'I am guilty': ")
  logger.debug(f"User response: {response}")

  if response != "I am guilty":
    print("Glad to see youre not guilty, the polar bears will thank you.")
    return
  else:
    shutil.rmtree(current_users_guilt_directory)
    print(f"{current_users_guilt_directory} was removed!")
    print("\nWaving goodbye from GUILT software.")
    
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("teardown")
  subparser.set_defaults(function=execute)