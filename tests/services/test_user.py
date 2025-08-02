from guilt.interfaces.services.user import UserServiceInterface
from guilt.services.user import UserService
from guilt.dependencies.injector import DependencyInjector
from pytest import MonkeyPatch
from subprocess import CompletedProcess
import subprocess
import getpass
import pytest

def resolve_user_service() -> UserServiceInterface:
  di = DependencyInjector()
  di.bind(UserServiceInterface, UserService)
  return di.resolve(UserServiceInterface)  # type: ignore[type-abstract]

def test_get_user_by_username(monkeypatch: MonkeyPatch) -> None:
  user_service = resolve_user_service()

  def mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout="guilt:x:1001:1001::/home/guilt:/bin/bash\notheruser:x:1002:1002::/home/otheruser:/bin/bash\n",
      stderr=""
    )

  monkeypatch.setattr(subprocess, "run", mock_run)

  results = user_service.get_user_by_username("guilt")

  assert results is not None
  assert results.username == "guilt"

def test_get_user_by_username_not_found(monkeypatch: MonkeyPatch) -> None:
  user_service = resolve_user_service()

  def mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout="",
      stderr=""
    )

  monkeypatch.setattr(subprocess, "run", mock_run)

  results = user_service.get_user_by_username("nonexistentuser")

  assert results is None

def test_get_all_users(monkeypatch: MonkeyPatch) -> None:
  user_service = resolve_user_service()

  def mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout="root:x:0:0:root:/root:/bin/bash\nguilt:x:1001:1001::/home/guilt:/bin/bash\n",
      stderr=""
    )

  monkeypatch.setattr(subprocess, "run", mock_run)

  results = list(user_service.get_all_users())

  assert len(results) == 2
  assert results[0].username == "root"
  assert results[1].username == "guilt"

def test_get_current_user(monkeypatch: MonkeyPatch) -> None:
  user_service = resolve_user_service()

  def mock_getuser() -> str:
    return "guilt"

  monkeypatch.setattr(getpass, "getuser", mock_getuser)

  def mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
    return CompletedProcess(
      args=command,
      returncode=0,
      stdout=f"{mock_getuser()}:x:1001:1001::/home/{mock_getuser()}:/bin/bash\n",
      stderr=""
    )

  monkeypatch.setattr(subprocess, "run", mock_run)

  result = user_service.get_current_user()

  assert result is not None
  assert result.username == "guilt"

def test_get_all_users_raises(monkeypatch: MonkeyPatch) -> None:
  user_service = resolve_user_service()

  def mock_run(command: list[str], capture_output: bool, text: bool) -> CompletedProcess[str]:
    return CompletedProcess(
      args=command,
      returncode=1,
      stdout="",
      stderr="getent: command not found"
    )

  monkeypatch.setattr(subprocess, "run", mock_run)

  with pytest.raises(Exception):
    user_service.get_all_users()