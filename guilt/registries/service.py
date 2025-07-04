from guilt.services.setup import SetupService
from guilt.services.backfill import BackfillService
from dataclasses import dataclass

@dataclass
class ServiceRegistry:
  setup: SetupService
  backfill: BackfillService