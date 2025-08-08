from guilt.interfaces.models.unprocessed_job import UnprocessedJobInterface
from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from guilt.utility.json_reader import JsonReader
from guilt.types.json import Json
from typing import Optional

class LazyJsonUnprocessedJob(UnprocessedJobInterface):
  def __init__(self, data: Json, cpu_profile: CpuProfileInterface) -> None:
    self._data = JsonReader.expect_dict(data)
    self._cpu_profile = cpu_profile

    self._job_id: Optional[str] = None

  @property
  def job_id(self) -> str:
    if self._job_id is None:
      self._job_id = JsonReader.ensure_get_str(self._data, "job_id")
    return self._job_id

  @property
  def cpu_profile(self) -> CpuProfileInterface:
    return self._cpu_profile