from pathlib import Path
from guilt.interfaces.services.slurm_batch import SlurmBatchServiceInterface
import subprocess

class SlurmBatchService(SlurmBatchServiceInterface):
  def submit_job(self, file: Path) -> str:
    command: list[str] = ["sbatch", "--parsable", str(file)]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
      raise Exception(f"Command failed with error message: {result.stderr}")
    
    return result.stdout.strip()