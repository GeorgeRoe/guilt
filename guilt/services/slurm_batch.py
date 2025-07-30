from pathlib import Path
from guilt.interfaces.services.slurm_batch import SlurmBatchServiceInterface
import subprocess
from datetime import datetime
from typing import Optional
from guilt.mappers import map_to
from guilt.models.slurm_batch_test_result import SlurmBatchTestResult

class SlurmBatchService(SlurmBatchServiceInterface):
  def _add_begin_to_command(self, command: list[str], begin: datetime) -> None:
    command.extend(["--begin", begin.strftime("%Y-%m-%dT%H:%M:%S")])

  def submit_job(self, file: Path, begin: Optional[datetime]) -> str:
    command: list[str] = ["sbatch", "--parsable", str(file)]

    if begin is not None:
      self._add_begin_to_command(command, begin)

    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with error message: {result.stderr}")
    
    return result.stdout.strip()

  def test_job(self, file: Path, begin: Optional[datetime]) -> SlurmBatchTestResult:
    command: list[str] = ["sbatch", "--test-only", str(file)]

    if begin is not None:
      self._add_begin_to_command(command, begin)

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
      raise Exception(f"Command failed with error message: {result.stderr}")
    
    return map_to.slurm_batch_test_result.from_line(result.stderr.strip())