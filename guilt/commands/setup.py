from pathlib import Path
from guilt.constants import LOGO, CENTERED_TAGLINE

def setup_cmd(_):
  guilt_dir = Path.home() / ".guilt"

  if guilt_dir.exists():
    print("Error: GUILT has already been setup!")
    return

  print("\n\033[91m" + LOGO + "\n" * 2 + CENTERED_TAGLINE)
  print("\033[0m")

  print(f"Creating the {guilt_dir} directory")
  guilt_dir.mkdir(parents=True)