from pathlib import Path
from guilt.constants import LOGO, CENTERED_TAGLINE
from guilt.services.processed_jobs_data import ProcessedJobsDataService
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder

def execute(args: Namespace):
  guilt_dir = Path.home() / ".guilt"

  if guilt_dir.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  CpuProfilesConfigService.submit_data(CpuProfilesConfigService.get_default_data())
  ProcessedJobsDataService.submit_data(ProcessedJobsDataService.get_default_data())
  UnprocessedJobsDataService.submit_data(UnprocessedJobsDataService.get_default_data())
  
  print("GUILT is now setup!")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("setup")
  subparser.set_defaults(function=execute)