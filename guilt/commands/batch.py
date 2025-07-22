from pathlib import Path
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from typing import Union
from guilt.registries.service import ServiceRegistry

DIRECTIVE_START = "#GUILT --"

def execute(services: ServiceRegistry, args: Namespace):
  path = Path(args.input)
  logger.info(f"Processing batch input file: {path}")

  content = services.file_system.read_from_file(path).splitlines()

  directives: dict[str, Union[str, bool]] = {}
  for line in content:
    if not (line.startswith("#") or line == ""):
      break
    elif line.startswith(DIRECTIVE_START):
      directive = line.replace(DIRECTIVE_START, "").split("=")
      directives[directive[0]] = directive[1] if len(directive) == 2 else True
  logger.debug(f"Parsed directives: {directives}")

  picked_cpu_profile_name = directives.get("cpu-profile")
  if picked_cpu_profile_name is None:
    logger.warning("No CPU profile directive found in batch file")
  elif isinstance(picked_cpu_profile_name, bool):
    logger.error("Cpu profile directive must be a string")
    return

  cpu_profiles_config = services.cpu_profiles_config.read_from_file()
  
  cpu_profile = cpu_profiles_config.default
  if not picked_cpu_profile_name is None:
    found_cpu_profile = cpu_profiles_config.profiles.get(picked_cpu_profile_name)
    if found_cpu_profile is None:
      logger.error(f"CPU Profile '{picked_cpu_profile_name}' doesn't exist")
      return
    cpu_profile = found_cpu_profile
  
  job_id = services.slurm_batch.submit_job(path)
  logger.info(f"Job submitted with ID {job_id}")
  
  unprocessed_jobs_data = services.unprocessed_jobs_data.read_from_file()
  if job_id in unprocessed_jobs_data.jobs.keys():
    logger.error(f"Unprocessed job with job id '{job_id}' already exists.")
    return
  
  unprocessed_jobs_data.jobs[job_id] = UnprocessedJob(
    job_id,
    cpu_profile
  )
  services.unprocessed_jobs_data.write_to_file(unprocessed_jobs_data)
  logger.debug(f"Saved new unprocessed job with ID {job_id}")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("batch")
  subparser.add_argument("input", help="Input file or argument for batch command")
  subparser.set_defaults(function=execute)