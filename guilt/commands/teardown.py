import shutil
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry

def execute(services: ServiceRegistry, args: Namespace):
  if not services.file_system.does_path_exist(services.guilt_directory.get_guilt_directory_path()):
    logger.error("Error: GUILT has not been setup!")
    return

  print("\n\033[91mFeeling too guily?\033[0m\n")
  
  print(f"This command will permanently delete the following directory: {services.guilt_directory.get_guilt_directory_path()}")
  response = input("Confirm by typing the following: 'I am guilty': ")
  logger.debug(f"User response: {response}")

  if response != "I am guilty":
    print("Glad to see youre not guilty, the polar bears will thank you.")
    return
  else:
    services.file_system.remove_directory(services.guilt_directory.get_guilt_directory_path())
    print(f"{services.guilt_directory.get_guilt_directory_path()} was removed!")
    print("\nWaving goodbye from GUILT software.")
    
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("teardown")
  subparser.set_defaults(function=execute)