from pathlib import Path
import subprocess
from guilt.config.cpu_profiles import CpuProfilesConfig
from guilt.data.unprocessed_jobs import UnprocessedJobsData, UnprocessedJob
from guilt.log import logger

DIRECTIVE_START = "#GUILT --"

def execute(args):
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

  if content == None:
    logger.error(f"Failed to read file '{path}'")
    return

  directives = {}
  for line in content:
    if not (line.startswith("#") or line == ""):
      break
    elif line.startswith(DIRECTIVE_START):
      directive = line.replace(DIRECTIVE_START, "").split("=")
      directives[directive[0]] = directive[1] if len(directive) == 2 else True
  logger.debug(f"Parsed directives: {directives}")

  picked_cpu_profile_name = directives.get("cpu-profile")
  if picked_cpu_profile_name is None:
    logger.error("No CPU profile directive found in batch file")
    return

  cpu_profile = CpuProfilesConfig.from_file().get_profile(picked_cpu_profile_name)
  if cpu_profile is None:
    logger.error(f"CPU Profile '{picked_cpu_profile_name}' doesn't exist")
    return
  
  command = ["sbatch", "--parsable", args.input]
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
  
  unprocessed_jobs_data = UnprocessedJobsData()
  unprocessed_jobs_data.add_job(UnprocessedJob(
    job_id,
    cpu_profile
  ))
  unprocessed_jobs_data.save()
  logger.debug(f"Saved new unprocessed job with ID {job_id}")

def register_subparser(subparsers):
  subparser = subparsers.add_parser("batch")
  subparser.add_argument("input", help="Input file or argument for batch command")
  subparser.set_defaults(function=execute)