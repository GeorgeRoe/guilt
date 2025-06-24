from pathlib import Path
import shutil
from guilt.log import logger
from argparse import _SubParsersAction, Namespace

def execute(args: Namespace):
  guilt_dir = Path.home() / ".guilt"

  if not guilt_dir.exists():
    logger.error("Error: GUILT has not been setup!")
    return

  print("\n\033[91mFeeling too guily?\033[0m\n")
  
  print(f"This command will permanently delete the following directory: {guilt_dir}")
  response = input("Confirm by typing the following: 'I am guilty': ")
  logger.debug(f"User response: {response}")

  if response != "I am guilty":
    print("Glad to see youre not guilty, the polar bears will thank you.")
    return
  else:
    shutil.rmtree(guilt_dir)
    print(f"{guilt_dir} was removed!")
    print("\nWaving goodbye from GUILT software.")
    
def register_subparser(subparsers: _SubParsersAction):
  subparser = subparsers.add_parser("teardown")
  subparser.set_defaults(function=execute)