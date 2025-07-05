from guilt.repositories.environment_variables import EnvironmentVariablesRepository
from guilt.repositories.slurm_accounting import SlurmAccountingRepository

class PersonalSlurmAccounting:
  def __init__(
    self,
    environment_variables_repository: EnvironmentVariablesRepository,
    slurm_accounting_repository: SlurmAccountingRepository
  ):
    self.environment_variables_repository = environment_variables_repository
    self.slurm_accounting_repository = slurm_accounting_repository
  
  def get_all_jobs(self):
    username = self.environment_variables_repository.get_current_user()
    
    if username is None:
      raise ValueError("Username must have a value")
    
    return self.slurm_accounting_repository.getAllJobsForUser(username)