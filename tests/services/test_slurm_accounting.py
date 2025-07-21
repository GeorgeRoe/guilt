from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from guilt.services.slurm_accounting import SlurmAccountingService
from tests.mocks.services.environment_variables import MockEnvironmentVariablesService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.types.json import Json
from pathlib import Path
from pytest import MonkeyPatch
from datetime import datetime
import json
from dataclasses import dataclass
from subprocess import CompletedProcess
import subprocess
import pytest

@dataclass
class ExtendedSlurmAccountingResult(SlurmAccountingResult):
  user: str

EXAMPLE_RESULTS: list[ExtendedSlurmAccountingResult] = [
  ExtendedSlurmAccountingResult(
    job_id="1",
    start_time=datetime(2025, 1, 1),
    end_time=datetime(2025, 1 ,2),
    resources={
      "cpu": 4,
      "mem": 16000
    },
    user="some-user"
  ),
  ExtendedSlurmAccountingResult(
    job_id="2",
    start_time=datetime(2025, 1, 5),
    end_time=datetime(2025, 1, 7),
    resources={
      "cpu": 128,
      "mem": 128000
    },
    user="some-user"
  ),
  ExtendedSlurmAccountingResult(
    job_id="3",
    start_time=datetime(2025, 2, 1),
    end_time=datetime(2025, 2, 2),
    resources={
      "cpu": 8,
      "mem": 64000
    },
    user="other-user"
  )
]

def _extended_slurm_accounting_result_to_json(result: ExtendedSlurmAccountingResult) -> Json:
  return {
    "time": {
      "start": result.start_time.timestamp(),
      "end": result.end_time.timestamp()
    },
    "job_id": result.job_id,
    "tres": {
      "allocated": [
        {
          "type": name,
          "count": count
        }
        for name, count
        in result.resources.items()
      ]
    },
    "user": result.user
  }
  
def _mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
  stripped_command = [
    item for item in command
    if item != "sacct" and item != "--json"
  ]
  
  arguments: dict[str, str] = {}
  for i in range(len(stripped_command) // 2):
    arguments[stripped_command[2 * i].replace("--", "")] = stripped_command[2 * i + 1]
  
  filtered_results = EXAMPLE_RESULTS
  
  if "jobs" in arguments:
    job_ids = arguments["jobs"].split(",")
    filtered_results = [
      result for result in filtered_results
      if result.job_id in job_ids
    ]
    
  if "user" in arguments:
    user = arguments["user"]
    filtered_results = [
      result for result in filtered_results
      if result.user == user
    ]
    
  if "starttime" in arguments:
    start_time = datetime.strptime(arguments["starttime"], "%Y-%m-%d")
    filtered_results = [
      result for result in filtered_results
      if result.start_time > start_time
    ]
    
  return CompletedProcess(
    args=command,
    returncode=0,
    stdout=json.dumps({ "jobs": [
      _extended_slurm_accounting_result_to_json(result)
      for result in filtered_results
    ]}),
    stderr=""
  )

def test_get_jobs_with_ids(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, Path()))
  di.bind(SlurmAccountingServiceInterface, SlurmAccountingService)
  slurm_accounting_service = di.resolve(SlurmAccountingServiceInterface) # type: ignore[type-abstract]
  
  monkeypatch.setattr(subprocess, "run", _mock_run)
  
  job_ids = ["2", "3"]
  
  results = slurm_accounting_service.get_jobs_with_ids(job_ids)
  
  assert set([result.job_id for result in results]) == set(job_ids)
  
def test_get_users_jobs(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, Path()))
  di.bind(SlurmAccountingServiceInterface, SlurmAccountingService)
  slurm_accounting_service = di.resolve(SlurmAccountingServiceInterface) # type: ignore[type-abstract]
   
  monkeypatch.setattr(subprocess, "run", _mock_run)
  
  user = "some-user"
  
  results = slurm_accounting_service.get_users_jobs(user)
  
  assert set([
    result.job_id for result in results
  ]) == set([
    result.job_id
    for result in EXAMPLE_RESULTS
    if result.user == user
  ])
  
def test_get_current_users_jobs(monkeypatch: MonkeyPatch) -> None:
  user = "some-user"
  
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({"USER": user}, Path()))
  di.bind(SlurmAccountingServiceInterface, SlurmAccountingService)
  slurm_accounting_service = di.resolve(SlurmAccountingServiceInterface) # type: ignore[type-abstract]
  
  monkeypatch.setattr(subprocess, "run", _mock_run)
  
  results = slurm_accounting_service.get_current_users_jobs()
  
  assert set([
    result.job_id for result in results
  ]) == set([
    result.job_id
    for result in EXAMPLE_RESULTS
    if result.user == user
  ])
  
def test_get_failure(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, Path()))
  di.bind(SlurmAccountingServiceInterface, SlurmAccountingService)
  slurm_accounting_service = di.resolve(SlurmAccountingServiceInterface) # type: ignore[type-abstract]

  def mock_run(command: list[str], capture_output: bool, text: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
      args=command,
      returncode=1,
      stdout="",
      stderr="sacct: command not found"
    )
    
  monkeypatch.setattr(subprocess, "run", mock_run)
    
  with pytest.raises(Exception):
    slurm_accounting_service.get_users_jobs("")