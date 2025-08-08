from datetime import datetime

class SlurmBatchTestResult:
  def __init__(
    self,
    job_id: str,
    start_time: datetime,
    processor_count: int,
    nodes: str,
    partition: str
  ) -> None:
    self._job_id = job_id
    self._start_time = start_time
    self._processor_count = processor_count
    self._nodes = nodes
    self._partition = partition

  @property
  def job_id(self) -> str:
    return self._job_id
  
  @property
  def start_time(self) -> datetime:
    return self._start_time
  
  @property
  def processor_count(self) -> int:
    return self._processor_count
  
  @property
  def nodes(self) -> str:
    return self._nodes
  
  @property
  def partition(self) -> str:
    return self._partition