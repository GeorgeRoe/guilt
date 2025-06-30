from datetime import datetime

class SlurmAccountingResult:
  def __init__(
    self,
    job_id: str,
    start_time: datetime,
    end_time: datetime,
    resources: dict[str, float]
  ) -> None:
    self.job_id = job_id
    self.start_time = start_time
    self.end_time = end_time
    self.resources = resources
    
  def __repr__(self) -> str:
    return (
      f"SlurmAccountingResult(job_id={self.job_id}, "
      f"start_time={self.start_time}, "
      f"end_time={self.end_time}, "
      f"resources={self.resources})"
    )