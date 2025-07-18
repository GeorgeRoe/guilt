from pytest import MonkeyPatch
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from guilt.services.environment_variables import EnvironmentVariablesService
from guilt.dependencies.injector import DependencyInjector
from pathlib import Path
import pytest
import os

def resolve_environment_variables_service() -> EnvironmentVariablesServiceInterface:
  di = DependencyInjector()
  di.bind(EnvironmentVariablesServiceInterface, EnvironmentVariablesService)
  return di.resolve(EnvironmentVariablesServiceInterface) # type: ignore[type-abstract]

def test_get_variable_existing(monkeypatch: MonkeyPatch) -> None:
  monkeypatch.setenv("FOO", "bar")
  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.get_variable("FOO")
  assert result == "bar"
  
def test_get_variable_missing(monkeypatch: MonkeyPatch) -> None:
  monkeypatch.delenv("FOO", raising=False)
  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.get_variable("FOO")
  assert result is None
  
def test_ensure_get_variable_existing(monkeypatch: MonkeyPatch) -> None:
  monkeypatch.setenv("FOO", "bar")
  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.ensure_get_variable("FOO")
  assert result == "bar"
  
def test_ensure_get_variable_missing_raises(monkeypatch: MonkeyPatch) -> None:
  monkeypatch.delenv("FOO", raising=False)
  environment_variables_service = resolve_environment_variables_service()
  
  with pytest.raises(ValueError):
    environment_variables_service.ensure_get_variable("FOO")
  
def test_get_user(monkeypatch: MonkeyPatch) -> None:
  username = "guilt-testing"
  monkeypatch.setenv("USER", username)
  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.get_user()
  assert result == username
  
def test_get_home_directory_using_environment_variable(monkeypatch: MonkeyPatch) -> None:
  path = Path("/home/guilt-testing")
  monkeypatch.setenv("HOME", str(path))
  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.get_home_directory()
  assert result == path
  
def test_get_home_directory_using_tilda(monkeypatch: MonkeyPatch) -> None:
  monkeypatch.delenv("HOME", raising=False)

  fake_home = "/tmp/fake-home"
  
  def fake_expanduser(path: str) -> str:
    return path.replace("~", fake_home)

  monkeypatch.setattr(os.path, "expanduser", fake_expanduser)

  environment_variables_service = resolve_environment_variables_service()
  result = environment_variables_service.get_home_directory()

  assert result == Path(fake_home).resolve()