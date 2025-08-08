from guilt.interfaces.models.processed_job import ProcessedJobInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json
from typing import Optional
from datetime import datetime

class LazyJsonProcessedJob(ProcessedJobInterface):
  def __init__(self, data: Json, cpu_profile: CpuProfileInterface) -> None:
    self._data = JsonReader.expect_dict(data)
    self._cpu_profile = cpu_profile

    self._start: Optional[datetime] = None
    self._end: Optional[datetime] = None
    self._job_id: Optional[str] = None
    self._energy: Optional[float] = None
    self._emissions: Optional[float] = None
    self._generation_mix: Optional[dict[str, float]] = None

  @property
  def start(self) -> datetime:
    if self._start is None:
      self._start = datetime.fromisoformat(JsonReader.ensure_get_str(self._data, "start"))
    return self._start
  
  @property
  def end(self) -> datetime:
    if self._end is None:
      self._end = datetime.fromisoformat(JsonReader.ensure_get_str(self._data, "end"))
    return self._end

  @property
  def job_id(self) -> str:
    if self._job_id is None:
      self._job_id = JsonReader.ensure_get_str(self._data, "job_id")
    return self._job_id

  @property
  def cpu_profile(self) -> CpuProfileInterface:
    return self._cpu_profile

  @property
  def energy(self) -> float:
    if self._energy is None:
      self._energy = float(JsonReader.ensure_get_number(self._data, "energy"))
    return self._energy

  @property
  def emissions(self) -> float:
    if self._emissions is None:
      self._emissions = float(JsonReader.ensure_get_number(self._data, "emissions"))
    return self._emissions

  @property
  def generation_mix(self) -> dict[str, float]:
    if self._generation_mix is None:
      self._generation_mix = {
        JsonReader.expect_str(source): float(JsonReader.expect_number(value))
        for source, value
        in JsonReader.ensure_get_dict(self._data, "generation_mix").items()
      }
    return self._generation_mix