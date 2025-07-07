from guilt.interfaces.services.setup import SetupServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData

class SetupService(SetupServiceInterface):
  def __init__(
    self,
    cpu_profiles_config_service: CpuProfilesConfigServiceInterface,
    processed_jobs_data_service: ProcessedJobsDataServiceInterface,
    unprocessed_jobs_data_service: UnprocessedJobsDataServiceInterface
  ):
    self.cpu_profiles_config_service = cpu_profiles_config_service
    self.processed_jobs_data_service = processed_jobs_data_service
    self.unprocessed_jobs_data_service = unprocessed_jobs_data_service
  
  def setup_cpu_profiles_config_file(self) -> bool:
    try:
      self.cpu_profiles_config_service.write_to_file(self.cpu_profiles_config_service.get_default())
      return True
    except Exception:
      return False

  def setup_processed_jobs_data_file(self) -> bool:
    try:
      self.processed_jobs_data_service.write_to_file(ProcessedJobsData({}))
      return True
    except Exception:
      return False
    
  def setup_unprocessed_jobs_data_file(self) -> bool:
    try:
      self.unprocessed_jobs_data_service.write_to_file(UnprocessedJobsData({}))
      return True
    except Exception:
      return False
    
  def setup_all_files(self) -> bool:
    if not self.setup_cpu_profiles_config_file():
      return False
    
    if not self.setup_processed_jobs_data_file():
      return False
    
    if not self.setup_unprocessed_jobs_data_file():
      return False
    
    return True