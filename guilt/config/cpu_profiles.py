from pathlib import Path
import json

DEFAULT_DATA = {
  "default": "AMD EPYC 9654",
  "profiles": {
    "AMD EPYC 9654": {
      "tdp": 360,
      "cores": 96
    }
  }
}

PATH = Path.home() / ".guilt" / "cpu_profiles.json"

class CpuProfile:
  def __init__(self, name: str, tdp: int, cores: int):
    self.name = name
    self.tdp = tdp
    self.cores = cores
  
  @property
  def tdp_per_core(self):
    return self.tdp / self.cores

  def __repr__(self):
    return (
        f"CpuProfile(name='{self.name}', "
        f"tdp={self.tdp}, "
        f"cores={self.cores}, "
        f"tdp_per_core={self.tdp_per_core:.2f})"
    )

  def __eq__(self, other):
    if not isinstance(other, CpuProfile):
      return NotImplemented
    return (
      self.name == other.name and
      self.tdp == other.tdp and
      self.cores == other.cores
    )

class CpuProfilesConfig:
  def __init__(self):
    data = DEFAULT_DATA

    if PATH.exists():
      with PATH.open("r") as file:
        data = json.load(file)

    self.profiles = {}
    for name, specs in data.get("profiles").items():
      self.profiles[name] = CpuProfile(name, specs.get("tdp"), specs.get("cores"))

    self.default = self.profiles.get(data.get("default"))

  def get_profile(self, name: str):
    return self.profiles.get(name)

  def add_profile(self, profile: CpuProfile) -> bool:
    if not self.profiles.get(profile.name) is None:
      return False

    self.profiles[profile.name] = profile

    self.save()

    return True

  def remove_profile(self, profile: CpuProfile) -> bool:
    if profile == self.profiles.get(profile.name):
      self.profiles.pop(profile.name)
      self.save()
      return True

    return False

  def update_profile(self, profile: CpuProfile) -> bool:
    if not self.profiles.get(profile.name) is None:
      self.profiles[profile.name] = profile
      self.save()
      return True

    return False

  def save(self):
    data = {
      "default": self.default.name,
      "profiles": { profile.name: {
        "tdp": profile.tdp,
        "cores": profile.cores
      } for profile in self.profiles.values()}
    }

    PATH.parent.mkdir(parents=True, exist_ok=True)

    with PATH.open("w") as file:
      json.dump(data, file, indent=2)