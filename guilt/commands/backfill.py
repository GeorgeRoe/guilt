from guilt.data.unprocessed_jobs import UnprocessedJobsData
from guilt.config.cpu_profiles import CpuProfilesConfig
from guilt.log import logger
import os
from guilt.services.slurm_accounting import SlurmAccountingService
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.mappers.slurm_accounting_result import FromSlurmAccountingResult

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
    
  unprocessed_jobs_data = UnprocessedJobsData.from_file()
  cpu_profiles_config = CpuProfilesConfig.from_file()
  
  for result in SlurmAccountingService.getAllJobsForUser(user):
    unprocessed_job = FromSlurmAccountingResult.to_unprocessed_job(result, cpu_profiles_config.default)
    unprocessed_jobs_data.add_job(unprocessed_job)
    
  unprocessed_jobs_data.save()
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)