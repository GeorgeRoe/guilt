from guilt.data.unprocessed_jobs import UnprocessedJobsData, UnprocessedJob
from guilt.config.cpu_profiles import CpuProfilesConfig
from guilt.log import logger
import os
from guilt.services.slurm_accounting import SlurmAccountingService
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
  
  jobs = SlurmAccountingService.getAllJobsForUser(user)
  
  unprocessed_jobs_data = UnprocessedJobsData.from_file()
  cpu_profiles_config = CpuProfilesConfig.from_file()
  
  for job in jobs:
    unprocessed_jobs_data.add_job(UnprocessedJob(
      job.job_id,
      cpu_profiles_config.default
    ))
    
  unprocessed_jobs_data.save()
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)