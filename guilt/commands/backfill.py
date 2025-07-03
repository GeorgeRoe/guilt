from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository
from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.log import logger
import os
from guilt.repositories.slurm_accounting import SlurmAccountingRepository
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.mappers.unprocessed_job import MapToUnprocessedJob

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
    
  unprocessed_jobs_data = UnprocessedJobsDataRepository.fetch_data()
  cpu_profiles_config = CpuProfilesConfigRepository.fetch_data()
  
  for result in SlurmAccountingRepository.getAllJobsForUser(user):
    unprocessed_job = MapToUnprocessedJob.from_slurm_accounting_result(result, cpu_profiles_config.default)
    
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job
    
  UnprocessedJobsDataRepository.submit_data(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)