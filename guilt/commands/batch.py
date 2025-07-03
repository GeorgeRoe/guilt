from pathlib import Path
import subprocess
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.utility.safe_get import safe_get_string
from typing import Union

DIRECTIVE_START = "#GUILT --"

def execute(args: Namespace):
  path = Path(args.input)
  logger.info(f"Processing batch input file: {path}")

  content = None
  try:
    with path.open("r") as file:
      content = file.read().splitlines()
    logger.debug(f"Read {len(content)} lines from {path}")
  except Exception as e:
    logger.error(f"Failed to read file '{path}': {e}")
    return

  directives: dict[str, Union[str, bool]] = {}
  for line in content:
    if not (line.startswith("#") or line == ""):
      break
    elif line.startswith(DIRECTIVE_START):
      directive = line.replace(DIRECTIVE_START, "").split("=")
      directives[directive[0]] = directive[1] if len(directive) == 2 else True
  logger.debug(f"Parsed directives: {directives}")

  try:
    picked_cpu_profile_name = safe_get_string(directives, "cpu-profile")
  except:
    logger.error("No CPU profile directive found in batch file")
    return

  cpu_profile = CpuProfilesConfigService.fetch_data().profiles.get(picked_cpu_profile_name)
  if cpu_profile is None:
    logger.error(f"CPU Profile '{picked_cpu_profile_name}' doesn't exist")
    return
  
  command = ["sbatch", "--parsable", str(args.input)]
  logger.info(f"Running command: {' '.join(command)}")
  try:
    result = subprocess.run(command, capture_output=True, text=True)
  except Exception as e:
    logger.error(f"Error running command '{' '.join(command)}': {e}")
    return
  
  if result.returncode != 0:
    logger.error(f"Command failed with code {result.returncode}: {result.stderr.strip()}")
    return
  
  job_id = result.stdout.strip()
  logger.info(f"Job submitted with ID {job_id}")
  
  unprocessed_jobs_data = UnprocessedJobsDataService.fetch_data()
  if job_id in unprocessed_jobs_data.jobs.keys():
    logger.error(f"Unprocessed job with job id '{job_id}' already exists.")
    return
  
  unprocessed_jobs_data.jobs[job_id] = UnprocessedJob(
    job_id,
    cpu_profile
  )
  UnprocessedJobsDataService.submit_data(unprocessed_jobs_data)
  logger.debug(f"Saved new unprocessed job with ID {job_id}")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("batch")
  subparser.add_argument("input", help="Input file or argument for batch command")
  subparser.set_defaults(function=execute)