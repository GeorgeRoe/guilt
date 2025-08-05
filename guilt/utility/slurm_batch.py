from guilt.models.slurm_batch_test_result import SlurmBatchTestResult
from guilt.mappers import map_to
from datetime import datetime
from typing import Optional
from pathlib import Path
import subprocess

def _construct_command(
  file: Path,
  begin: Optional[datetime] = None,
  test: bool = False
) -> list[str]:
  command = ["sbatch"]
  
  if test:
    command.append("--test-only")

  if begin:
    command.append("--begin")
    command.append(begin.strftime("%Y-%m-%dT%H:%M:%S"))

  command.append(str(file))

  return command

def _run_command(command: list[str]) -> str:
  result = subprocess.run(command, capture_output=True, text=True)

  if result.returncode != 0:
    raise Exception(f"Command failed with code {result.returncode}: {result.stderr.strip()}")

  return result.stdout.strip()

def submit(file: Path, begin: Optional[datetime] = None) -> str:
  return _run_command(_construct_command(file, begin))

def test(file: Path, begin: Optional[datetime] = None) -> SlurmBatchTestResult:
  return map_to.slurm_batch_test_result.from_line(_run_command(_construct_command(file, begin, test=True))