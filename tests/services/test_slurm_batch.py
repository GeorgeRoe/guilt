from guilt.interfaces.services.slurm_batch import SlurmBatchServiceInterface
from guilt.services.slurm_batch import SlurmBatchService
from guilt.dependencies.injector import DependencyInjector
from pytest import MonkeyPatch
from subprocess import CompletedProcess
import subprocess
import pytest
from pathlib import Path

def test_submit_job_success(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.bind(SlurmBatchServiceInterface, SlurmBatchService)
  slurm_batch_service = di.resolve(SlurmBatchServiceInterface) # type: ignore[type-abstract]  
  
  def mock_run(command: list[str], capture_output: bool, text: bool):
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout="1",
      stderr=""
    )
    
  monkeypatch.setattr(subprocess, "run", mock_run)
  
  result = slurm_batch_service.submit_job(Path())
  
  assert result == "1"

def test_submit_job_raises(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.bind(SlurmBatchServiceInterface, SlurmBatchService)
  slurm_batch_service = di.resolve(SlurmBatchServiceInterface) # type: ignore[type-abstract]
  
  def mock_run(command: list[str], capture_output: bool, text: bool):
    return CompletedProcess(
      args=command,
      returncode=1,
      stdout="",
      stderr="sbatch: command not found"
    )
    
  monkeypatch.setattr(subprocess, "run", mock_run)
  
  with pytest.raises(Exception):
    slurm_batch_service.submit_job(Path())