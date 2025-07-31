from typing import Optional
from guilt.parsers import parse_slurm_accounting_json
from guilt.types.json import Json
from datetime import datetime

class LazySlurmAccountingResult:
  def __init__(self, data: dict[str, Json]) -> None:
    self._data = data

    self._job_id: Optional[str] = None
    self._start_time: Optional[datetime] = None
    self._end_time: Optional[datetime] = None
    self._resources: Optional[dict[str, float]] = None

  @property
  def job_id(self) -> str:
    if self._job_id is None:
      self._job_id = parse_slurm_accounting_json.get_job_id(self._data)
    return self._job_id
  
  @property
  def start_time(self) -> datetime:
    if self._start_time is None:
      self._start_time = parse_slurm_accounting_json.get_start_time(self._data)
    return self._start_time
  
  @property
  def end_time(self) -> datetime:
    if self._end_time is None:
      self._end_time = parse_slurm_accounting_json.get_end_time(self._data)
    return self._end_time
  
  @property
  def resources(self) -> dict[str, float]:
    if self._resources is None:
      self._resources = parse_slurm_accounting_json.get_resources(self._data)
    return self._resources