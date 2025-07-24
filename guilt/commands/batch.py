from pathlib import Path
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry
from guilt.mappers import map_to

DIRECTIVE_START = "#GUILT --"

def execute(services: ServiceRegistry, args: Namespace):
  path = Path(args.input)
  logger.info(f"Processing batch input file: {path}")

  content = services.file_system.read_from_file(path).splitlines()

  guilt_directives = map_to.guilt_script_directives.from_json_directives(
    map_to.json.from_directive_lines(content, "#SBATCH"),
    services.cpu_profiles_config.read_from_file()
  )
  
  job_id = services.slurm_batch.submit_job(path)
  logger.info(f"Job submitted with ID {job_id}")
  
  unprocessed_jobs_data = services.unprocessed_jobs_data.read_from_file()
  if job_id in unprocessed_jobs_data.jobs.keys():
    logger.error(f"Unprocessed job with job id '{job_id}' already exists.")
    return
  
  unprocessed_jobs_data.jobs[job_id] = UnprocessedJob(
    job_id,
    guilt_directives.cpu_profile
  )
  services.unprocessed_jobs_data.write_to_file(unprocessed_jobs_data)
  logger.debug(f"Saved new unprocessed job with ID {job_id}")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("batch")
  subparser.add_argument("input", help="Input file or argument for batch command")
  subparser.set_defaults(function=execute)