from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from guilt.log import logger
import os
from guilt.services.slurm_accounting import SlurmAccountingService
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.mappers.unprocessed_job import MapToUnprocessedJob

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
    
  unprocessed_jobs_data = UnprocessedJobsDataService.fetch_data()
  cpu_profiles_config = CpuProfilesConfigService.fetch_data()
  
  for result in SlurmAccountingService.getAllJobsForUser(user):
    unprocessed_job = MapToUnprocessedJob.from_slurm_accounting_result(result, cpu_profiles_config.default)
    
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job
    
  UnprocessedJobsDataService.submit_data(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)