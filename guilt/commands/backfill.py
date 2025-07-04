from guilt.log import logger
import os
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependencies.manager import dependency_manager

unprocessed_jobs_data_repository = dependency_manager.repository.unprocessed_jobs_data
slurm_accounting_repository = dependency_manager.repository.slurm_accounting

backfill_service = dependency_manager.service.backfill

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
    
  unprocessed_jobs_data = unprocessed_jobs_data_repository.fetch_data()
  
  all_historical_user_jobs = slurm_accounting_repository.getAllJobsForUser(user)
  
  converted_unprocessed_jobs = backfill_service.convert_slurm_jobs_to_unprocessed_jobs(all_historical_user_jobs)
  
  for unprocessed_job in converted_unprocessed_jobs:
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job
      
  unprocessed_jobs_data_repository.submit_data(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)