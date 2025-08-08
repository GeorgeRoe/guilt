from guilt.interfaces.models.unprocessed_job import UnprocessedJobInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface

class UnprocessedJob(UnprocessedJobInterface):
  def __init__(self, job_id: str, cpu_profile: CpuProfileInterface) -> None:
    self._job_id = job_id
    self._cpu_profile = cpu_profile

  @property
  def job_id(self) -> str:
    return self._job_id

  @property
  def cpu_profile(self) -> CpuProfileInterface:
    return self._cpu_profile