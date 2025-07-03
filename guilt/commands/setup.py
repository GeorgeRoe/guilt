from pathlib import Path
from guilt.constants import LOGO, CENTERED_TAGLINE
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependency_manager import dependency_manager

cpu_profiles_config_repository = dependency_manager.repository.cpu_profiles_config
processed_jobs_data_repository = dependency_manager.repository.processed_jobs_data
unprocessed_jobs_data_repository = dependency_manager.repository.unprocessed_jobs_data

def execute(args: Namespace):
  guilt_dir = Path.home() / ".guilt"

  if guilt_dir.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  cpu_profiles_config_repository.submit_data(cpu_profiles_config_repository.get_default_data())
  processed_jobs_data_repository.submit_data(processed_jobs_data_repository.get_default_data())
  unprocessed_jobs_data_repository.submit_data(unprocessed_jobs_data_repository.get_default_data())
  
  print("GUILT is now setup!")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("setup")
  subparser.set_defaults(function=execute)