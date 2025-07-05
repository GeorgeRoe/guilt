from guilt.registries.repository import RepositoryRegistry
from guilt.registries.service import ServiceRegistry
from guilt.services.setup import SetupService
from guilt.services.backfill import BackfillService
from guilt.services.personal_slurm_accounting import PersonalSlurmAccounting
from dataclasses import dataclass

@dataclass
class DependencyManager:
  repository: RepositoryRegistry
  service: ServiceRegistry
  
def construct_default_dependency_manager() -> DependencyManager:
  repositories = RepositoryRegistry()
  
  services = ServiceRegistry(
    SetupService(
      repositories.cpu_profiles_config,
      repositories.processed_jobs_data,
      repositories.unprocessed_jobs_data
    ),
    BackfillService(
      repositories.cpu_profiles_config
    ),
    PersonalSlurmAccounting(
      repositories.environment_varialbes,
      repositories.slurm_accounting
    )
  )
  
  return DependencyManager(repositories, services)

dependency_manager = construct_default_dependency_manager()