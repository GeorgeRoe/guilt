from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.repositories.processed_jobs_data import ProcessedJobsDataRepository
from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository

class SetupService:
  def __init__(
    self,
    cpu_profiles_config_repository: CpuProfilesConfigRepository,
    processed_jobs_data_repository: ProcessedJobsDataRepository,
    unprocessed_jobs_data_repository: UnprocessedJobsDataRepository
  ):
    self.cpu_profiles_config_repository = cpu_profiles_config_repository
    self.processed_jobs_data_repository = processed_jobs_data_repository
    self.unprocessed_jobs_data_repository = unprocessed_jobs_data_repository
  
  def setup_cpu_profiles(self) -> bool:
    try:
      self.cpu_profiles_config_repository.submit_data(self.cpu_profiles_config_repository.get_default_data())
      return True
    except Exception:
      return False

  def setup_processed_jobs(self) -> bool:
    try:
      self.processed_jobs_data_repository.submit_data(self.processed_jobs_data_repository.get_default_data())
      return True
    except Exception:
      return False

  def setup_unprocessed_jobs(self) -> bool:
    try:
      self.unprocessed_jobs_data_repository.submit_data(self.unprocessed_jobs_data_repository.get_default_data())
      return True
    except Exception:
      return False
    
  def setup_all(self) -> bool:
    if not self.setup_cpu_profiles():
      return False
    
    if not self.setup_processed_jobs():
      return False
    
    if not self.setup_unprocessed_jobs():
      return False
    
    return True