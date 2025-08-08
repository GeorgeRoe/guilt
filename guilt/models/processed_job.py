from guilt.interfaces.models.processed_job import ProcessedJobInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from datetime import datetime

class ProcessedJob(ProcessedJobInterface):
  def __init__(
    self,
    start: datetime,
    end: datetime,
    job_id: str,
    cpu_profile: CpuProfileInterface,
    energy: float,
    emissions: float,
    generation_mix: dict[str, float]
  ) -> None:
    self._start = start
    self._end = end
    self._job_id = job_id
    self._cpu_profile = cpu_profile
    self._energy = energy
    self._emissions = emissions
    self._generation_mix = generation_mix

  @property
  def start(self) -> datetime:
    return self._start
  
  @property
  def end(self) -> datetime:
    return self._end
  
  @property
  def job_id(self) -> str:
    return self._job_id
  
  @property
  def cpu_profile(self) -> CpuProfileInterface:
    return self._cpu_profile
  
  @property
  def energy(self) -> float:
    return self._energy
  
  @property
  def emissions(self) -> float:
    return self._emissions
  
  @property
  def generation_mix(self) -> dict[str, float]:
    return self._generation_mix