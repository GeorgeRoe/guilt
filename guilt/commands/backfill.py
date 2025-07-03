from guilt.log import logger
import os
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.mappers.unprocessed_job import MapToUnprocessedJob
from guilt.dependencies.manager import dependency_manager

unprocessed_jobs_data_repository = dependency_manager.repository.unprocessed_jobs_data
cpu_profiles_config_repository = dependency_manager.repository.cpu_profiles_config
slurm_accounting_repository = dependency_manager.repository.slurm_accounting

def execute(args: Namespace):
  user = os.getenv("USER", None)
  if user is None:
    logger.error("Couldn't get user environment variable")
    return
    
  unprocessed_jobs_data = unprocessed_jobs_data_repository.fetch_data()
  cpu_profiles_config = cpu_profiles_config_repository.fetch_data()
  
  for result in slurm_accounting_repository.getAllJobsForUser(user):
    unprocessed_job = MapToUnprocessedJob.from_slurm_accounting_result(result, cpu_profiles_config.default)
    
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job
    
  unprocessed_jobs_data_repository.submit_data(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)