from pathlib import Path
from guilt.constants import LOGO, CENTERED_TAGLINE
from guilt.repositories.processed_jobs_data import ProcessedJobsDataRepository
from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository
from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder

def execute(args: Namespace):
  guilt_dir = Path.home() / ".guilt"

  if guilt_dir.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  CpuProfilesConfigRepository.submit_data(CpuProfilesConfigRepository.get_default_data())
  ProcessedJobsDataRepository.submit_data(ProcessedJobsDataRepository.get_default_data())
  UnprocessedJobsDataRepository.submit_data(UnprocessedJobsDataRepository.get_default_data())
  
  print("GUILT is now setup!")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("setup")
  subparser.set_defaults(function=execute)