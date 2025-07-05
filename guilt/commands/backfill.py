from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependencies.manager import dependency_manager

unprocessed_jobs_data_repository = dependency_manager.repository.unprocessed_jobs_data

backfill_service = dependency_manager.service.backfill
personal_slurm_accounting = dependency_manager.service.personal_slurm_accounting

def execute(args: Namespace):   
  all_historical_user_jobs = personal_slurm_accounting.get_all_jobs()
  converted_unprocessed_jobs = backfill_service.convert_slurm_jobs_to_unprocessed_jobs(all_historical_user_jobs)
  
  unprocessed_jobs_data = unprocessed_jobs_data_repository.fetch_data()
  
  for unprocessed_job in converted_unprocessed_jobs:
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job
      
  unprocessed_jobs_data_repository.submit_data(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)