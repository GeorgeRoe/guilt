from guilt.interfaces.services.get_entries_password import GetEntriesPasswordServiceInterface
from guilt.services.get_entries_password import GetEntriesPasswordService
from guilt.dependencies.injector import DependencyInjector
from pytest import MonkeyPatch
from subprocess import CompletedProcess
import subprocess
import pytest

def test_get_entries_success(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.bind(GetEntriesPasswordServiceInterface, GetEntriesPasswordService)
  get_entries_password_service = di.resolve(GetEntriesPasswordServiceInterface) # type: ignore[type-abstract]
  
  def mock_run(command: list[str], capture_output: bool, text: bool):
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout="root:x:0:0:root:/root:/bin/bash\nguilt:x:1001:1001::/home/guilt:/bin/bash\n",
      stderr=""
    )
    
  monkeypatch.setattr(subprocess, "run", mock_run)
  
  results = get_entries_password_service.get_entries()
  
  assert len(results) == 2
  assert results[0].username == "root"
  assert results[1].username == "guilt"
  
def test_get_entries_raises(monkeypatch: MonkeyPatch) -> None:
  di = DependencyInjector()
  di.bind(GetEntriesPasswordServiceInterface, GetEntriesPasswordService)
  get_entries_password_service = di.resolve(GetEntriesPasswordServiceInterface) # type: ignore[type-abstract]
  
  def mock_run(command: list[str], capture_output: bool, text: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
      args=command,
      returncode=1,
      stdout="",
      stderr="getent: command not found"
    )
    
  monkeypatch.setattr(subprocess, "run", mock_run)
  
  with pytest.raises(Exception):
    get_entries_password_service.get_entries()