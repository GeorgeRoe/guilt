from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry

def execute(services: ServiceRegistry, args: Namespace):
  all_historical_user_jobs = services.slurm_accounting.get_current_users_jobs()
  converted_unprocessed_jobs = services.backfill.convert_slurm_jobs_to_unprocessed_jobs(all_historical_user_jobs)
  
  unprocessed_jobs_data = services.unprocessed_jobs_data.read_from_file()
  
  for unprocessed_job in converted_unprocessed_jobs:
    if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
      unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job

  services.unprocessed_jobs_data.write_to_file(unprocessed_jobs_data)
  
def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("backfill")
  subparser.set_defaults(function=execute)