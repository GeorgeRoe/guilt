from guilt.constants.branding import LOGO, CENTERED_TAGLINE
from guilt.constants.paths import GUILT_DIRECTORY
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependencies.manager import dependency_manager

setup_service = dependency_manager.service.setup

def execute(args: Namespace):
  if GUILT_DIRECTORY.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  setup_service.setup_all()
  
  print("GUILT is now setup!")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("setup")
  subparser.set_defaults(function=execute)