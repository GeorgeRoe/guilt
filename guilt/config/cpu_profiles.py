from pathlib import Path
import json
from guilt.log import logger

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

  @classmethod
  def from_dict(cls, data: dict):
    logger.debug(f"Deserializing CpuProfile: {data}")
    return cls(data.get("name"), data.get("tdp"), data.get("cores"))

  def to_dict(self) -> dict:
    return {
      "name": self.name,
      "tdp": self.tdp,
      "cores": self.cores
    }

class CpuProfilesConfig:
  def __init__(self):
    data = DEFAULT_DATA

    if PATH.exists():
      try:
        with PATH.open("r") as file:
          data = json.load(file)
        logger.info(f"Loaded CPU profiles from {PATH}")
      except Exception as e:
        logger.error(f"Failed to load CPU profiles from {PATH}: {e}")
        data = DEFAULT_DATA
    else:
      logger.info("No CPU profile config found, using default")

    self.profiles = {}
    for name, specs in data.get("profiles").items():
      profile_data = {
        "name": name,
        **specs
      }
      self.profiles[name] = CpuProfile.from_dict(profile_data)
      
    self.default = self.profiles.get(data.get("default"))
    logger.debug(f"Default CPU profile: {self.default}")

  def get_profile(self, name: str):
    logger.debug(f"Fetching CPU profile: {name}")
    return self.profiles.get(name)

  def add_profile(self, profile: CpuProfile) -> bool:
    if not self.profiles.get(profile.name) is None:
      logger.warning(f"Profile '{profile.name}' already exists, not adding")
      return False

    self.profiles[profile.name] = profile

    logger.info(f"Added new CPU profile: {profile}")
    self.save()

    return True

  def remove_profile(self, profile: CpuProfile) -> bool:
    if profile == self.profiles.get(profile.name):
      self.profiles.pop(profile.name)
      logger.info(f"Removed CPU profile: {profile.name}")
      self.save()
      return True

    logger.warning(f"Attempted to remove non-matching or nonexistent profile: {profile.name}")
    return False

  def update_profile(self, profile: CpuProfile) -> bool:
    if not self.profiles.get(profile.name) is None:
      self.profiles[profile.name] = profile
      logger.info(f"Updated CPU profile: {profile.name}")
      self.save()
      return True

    logger.warning(f"Attempted to update nonexistent profile: {profile.name}")
    return False

  def save(self):
    data = {
      "default": self.default.name,
      "profiles": {
        profile.name: {k:v for k, v in profile.to_dict().items() if k != "name"} 
        for profile in self.profiles.values()
      }
    }

    PATH.parent.mkdir(parents=True, exist_ok=True)
    
    try:
      with PATH.open("w") as file:
        json.dump(data, file, indent=2)
      logger.info(f"Saved CPU profiles to {PATH}")
    except Exception as e:
      logger.error(f"Failed to save CPU profiles to {PATH}: {e}")