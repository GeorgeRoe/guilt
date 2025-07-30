from guilt.models.slurm_batch_test_result import SlurmBatchTestResult
import re
from datetime import datetime


class MapToSlurmBatchTestResult:
    @staticmethod
    def from_line(line: str) -> SlurmBatchTestResult:
      pattern = re.compile(
        r"sbatch: Job (\d+) to start at ([\d\-T:]+) using (\d+) processors on nodes (.*?) in partition (\w+)"
      )

      match = pattern.match(line)

      if match:
        job_id = match.group(1)
        start_time_str = match.group(2)
        processor_count_str = match.group(3)
        nodes = match.group(4)
        partition = match.group(5)

        return SlurmBatchTestResult(
          job_id=job_id,
          start_time=datetime.fromisoformat(start_time_str),
          processor_count=int(processor_count_str),
          nodes=nodes,
          partition=partition
        )
      else:
        raise ValueError(f"Line does not match expected format: {line}")
        