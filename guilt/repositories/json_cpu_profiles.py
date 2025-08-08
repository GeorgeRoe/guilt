from guilt.interfaces.repositories.cpu_profiles import CpuProfilesRepositoryInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from guilt.models.lazy_json_cpu_profile import LazyJsonCpuProfile
from guilt.utility import json_reader
from guilt.types.json import Json
from typing import Optional, Sequence
from pathlib import Path
import json

class JsonCpuProfilesRepository(CpuProfilesRepositoryInterface):
  def __init__(self, path: Path) -> None:
    self._path = path

    self._profiles: dict[str, CpuProfileInterface] = {}
    with self._path.open("r") as file:
      raw_profiles = json_reader.expect_list(json.load(file))
      for profile in raw_profiles:
        lazy_profile = LazyJsonCpuProfile(profile)
        self._profiles[lazy_profile.name] = lazy_profile
  
  def get(self, name: str) -> Optional[CpuProfileInterface]:
    return self._profiles.get(name)

  def get_all(self) -> Sequence[CpuProfileInterface]:
    return list(self._profiles.values())
  
  def upsert(self, profile: CpuProfileInterface) -> None:
    self._profiles[profile.name] = profile

  def delete(self, name: str) -> None:
    if name in self._profiles:
      del self._profiles[name]

  def save(self) -> bool:
    raw_profiles: list[dict[str, Json]] = []

    for profile in self._profiles.values():
      raw_profiles.append({
        "name": profile.name,
        "tdp": profile.tdp,
        "cores": profile.cores
      })

    try:
      with self._path.open("w") as file:
        json.dump(raw_profiles, file, indent=2)
      return True
    except Exception:
      return False