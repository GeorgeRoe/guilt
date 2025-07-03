from guilt.services.setup import SetupService
from dataclasses import dataclass

@dataclass
class ServiceRegistry:
  setup: SetupService