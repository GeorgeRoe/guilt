from pathlib import Path
import subprocess
from guilt.config.cpu_profiles import CpuProfilesConfig
from guilt.data.unprocessed_jobs import UnprocessedJobsData, UnprocessedJob

DIRECTIVE_START = "#GUILT --"

def batch_cmd(args):
  path = Path(args.input)

  content = None
  try:
    with path.open("r") as file:
      content = file.read().splitlines()
  except:
    pass

  if content == None:
    print("Error reading file.")
    return

  directives = {}
  for line in content:
    if not (line.startswith("#") or line == ""):
      break
    elif line.startswith(DIRECTIVE_START):
      directive = line.replace(DIRECTIVE_START, "").split("=")
      directives[directive[0]] = directive[1] if len(directive) == 2 else True

  picked_cpu_profile_name = directives.get("cpu-profile")
  if picked_cpu_profile_name is None:
    print("No CPU profile given.")
    return

  cpu_profile = CpuProfilesConfig().get_profile(picked_cpu_profile_name)
  if cpu_profile is None:
    print(f"CPU Profile '{picked_cpu_profile_name}' doesn't exist")
  
  command = ["sbatch", "--parsable", args.input]
  result = subprocess.run(command, capture_output=True, text=True)
  
  if result.returncode != 0:
    print(f"The command '{' '.join(command)}' encountered an error:")
    print(result.stderr)
    return
  
  job_id = result.stdout.strip()
  
  print(f"Submitted job! (ID = {job_id})")
  
  unprocessed_jobs_data = UnprocessedJobsData()
  unprocessed_jobs_data.add_job(UnprocessedJob(
    job_id,
    cpu_profile
  ))