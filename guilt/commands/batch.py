from pathlib import Path
import subprocess

def batch_cmd(args):
  path = Path(args.input)

  content = None
  with path.open("r") as file:
    content = file.read().splitlines()

  directives = {}
  for line in content:
    print(line)

    if not (line.startswith("#") or line == ""):
      break
    elif line.startswith("#SBATCH --"):
      directive = line.replace("#SBATCH --", "").split("=")
      print(directive)
      directives[directive[0]] = directive[1] if len(directive) == 2 else True

  print(directives)

  # result = subprocess.run(["sbatch", args.input], capture_output=True, text=True)
  # print(result)