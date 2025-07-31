from guilt.interfaces.services.backfill import BackfillServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.services.backfill import BackfillService
from tests.mocks.services.cpu_profiles_config import MockCpuProfilesConfigService
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.dependencies.injector import DependencyInjector
from guilt.models.cpu_profile import CpuProfile
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from datetime import datetime

default_profile = CpuProfile("AMD EPYC 9654", 360, 96)
    
profiles = [
  default_profile,
  CpuProfile("AMD EPYC 7502", 180, 32),
  CpuProfile("AMD EPYC 7742", 225, 64),
  CpuProfile("AMD EPYC 7543P", 225, 32)
]
  
DEFAULT_CPU_PROFILES_CONFIG = CpuProfilesConfig(default_profile, {profile.name: profile for profile in profiles})

def test_convert_slurm_jobs_to_unprocessed_jobs() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.bind(BackfillServiceInterface, BackfillService)
  backfill_service = di.resolve(BackfillServiceInterface) # type: ignore[type-abstract]
  
  slurm_jobs: list[LazySlurmAccountingResult] = [
    LazySlurmAccountingResult({
      "job_id": "1",
      "time": {
        "start": datetime(2025, 1, 1).timestamp(),
        "end": datetime(2025, 1, 2).timestamp()
      },
      "tres": {
        "allocated": [
          {"type": "cpu", "count": 8},
          {"type": "mem", "count": 16000}
        ]
      }
    })
  ]
  
  result = backfill_service.convert_slurm_jobs_to_unprocessed_jobs(slurm_jobs)
  
  assert len(result) == 1
  
  item = result[0]
  
  assert item != None
  assert item.cpu_profile == DEFAULT_CPU_PROFILES_CONFIG.default
  assert item.job_id == "1"