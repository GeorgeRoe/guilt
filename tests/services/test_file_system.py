from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.services.file_system import FileSystemService
from guilt.dependencies.injector import DependencyInjector
from guilt.types.json import Json
from pathlib import Path

def resolve_file_system_service() -> FileSystemServiceInterface:
  di = DependencyInjector()
  di.bind(FileSystemServiceInterface, FileSystemService)
  return di.resolve(FileSystemServiceInterface) # type: ignore[type-abstract]

def test_does_path_exist(tmp_path: Path) -> None:
  file_system_service = resolve_file_system_service()
  
  test_file = tmp_path / "test.txt"
  assert not file_system_service.does_path_exist(test_file)
  test_file.write_text("hello")
  assert file_system_service.does_path_exist(test_file)
  
def test_create_directory(tmp_path: Path) -> None:
  file_system_service = resolve_file_system_service()
  
  new_dir = tmp_path / "nested" / "dir"
  assert not new_dir.exists()
  file_system_service.create_directory(new_dir)
  assert new_dir.exists()
  assert new_dir.is_dir()

def test_write_and_read_file(tmp_path: Path) -> None:
  file_system_service = resolve_file_system_service()
  
  file_path = tmp_path / "file.txt"
  content = "hello guilt"
  file_system_service.write_to_file(file_path, content)
  assert file_path.exists()
  read = file_system_service.read_from_file(file_path)
  assert read == content

def test_write_and_read_json(tmp_path: Path) -> None:
  file_system_service = resolve_file_system_service()
  
  file_path = tmp_path / "data.json"
  data: Json = {
    "key": "value",
    "numbers": [1, 2, 3]
  }
  file_system_service.write_to_json_file(file_path, data)
  assert file_path.exists()
  result = file_system_service.read_from_json_file(file_path)
  assert result == data