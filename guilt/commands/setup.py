from guilt.constants.branding import LOGO, CENTERED_TAGLINE
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry

def execute(services: ServiceRegistry, args: Namespace):
  if services.file_system.does_path_exist(services.guilt_directory.get_guilt_directory_path()):
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  if services.setup.setup_all_files():
    print("GUILT is now setup!")
  else:
    print("failed to setup GUILT.")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("setup")
  subparser.set_defaults(function=execute)