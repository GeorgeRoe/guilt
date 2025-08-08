from guilt.interfaces.repositories.settings import SettingsRepositoryInterface
from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from guilt.utility import json_reader
from typing import Optional
from pathlib import Path
import json

class JsonSettingsRepository(SettingsRepositoryInterface):
  def __init__(
    self,
    path: Path,
    cpu_profiles_repository: CpuProfilesRepositoryInterface
  ) -> None:
    self._path = path
    self._cpu_profiles_repository = cpu_profiles_repository
    
    self._default_cpu_profile: Optional[CpuProfileInterface] = None

    with self._path.open("r") as file:
      self._raw_settings = json_reader.expect_dict(json.load(file))

  def get_default_cpu_profile(self) -> Optional[CpuProfileInterface]:
    if self._default_cpu_profile is None:
      try:
        profile_name = json_reader.ensure_get_str(self._raw_settings, "default_cpu_profile")
        self._default_cpu_profile = self._cpu_profiles_repository.get(profile_name)
      except Exception:
        return None
    return self._default_cpu_profile

  def set_default_cpu_profile(self, cpu_profile: CpuProfileInterface) -> bool:
    fetched_profile = self._cpu_profiles_repository.get(cpu_profile.name)
    if fetched_profile is None:
      return False
    
    self._default_cpu_profile = fetched_profile
    return True

  def save(self) -> bool:
    if self._default_cpu_profile is None:
      return False

    self._raw_settings["default_cpu_profile"] = self._default_cpu_profile.name

    with self._path.open("w") as file:
      json.dump(self._raw_settings, file, indent=2)

    return True