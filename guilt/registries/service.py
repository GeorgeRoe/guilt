from guilt.services.setup import SetupService
from guilt.services.backfill import BackfillService
from guilt.services.personal_slurm_accounting import PersonalSlurmAccounting
from dataclasses import dataclass

@dataclass
class ServiceRegistry:
  setup: SetupService
  backfill: BackfillService
  personal_slurm_accounting: PersonalSlurmAccounting