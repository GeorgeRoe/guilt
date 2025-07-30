from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class WindowWithLowestSumResult:
  start_time: datetime
  sum_value: float

class TimeSeriesData:
  def __init__(self, points: dict[datetime, float]) -> None:
    self._points = dict(sorted(points.items()))
    self._times = sorted(self._points.keys())

  def get_first_time(self) -> datetime:
    if not self._times:
      raise ValueError("No data points available")
    return self._times[0]
  
  def get_last_time(self) -> datetime:
    if not self._times:
      raise ValueError("No data points available")
    return self._times[-1]

  def get_value_at(self, time: datetime) -> float:
    if time in self._points:
      return self._points[time]
    
    earlier_times = [t for t in self._times if t <= time]
    later_times = [t for t in self._times if t >= time]

    if not earlier_times or not later_times:
      raise ValueError(f"Time {time} out of range")

    previous_time = max(earlier_times)
    next_time = min(later_times)

    if previous_time == next_time:
      return self._points[previous_time]

    window_size = (next_time - previous_time).total_seconds()
    previous_value = self._points[previous_time]
    next_value = self._points[next_time]
    ratio = (time - previous_time).total_seconds() / window_size

    return previous_value + (next_value - previous_value) * ratio

  def get_window_sum(self, start_time: datetime, end_time: datetime) -> float:
    if start_time >= end_time:
      return 0.0

    total = 0.0
    current_time = start_time

    while current_time < end_time:
      future_times = [t for t in self._times if t > current_time]
      next_time = min(future_times, default=end_time)
      if next_time > end_time:
        next_time = end_time

      v1 = self.get_value_at(current_time)
      v2 = self.get_value_at(next_time)
      dt = (next_time - current_time).total_seconds()

      avg = (v1 + v2) / 2
      total += avg * dt

      current_time = next_time

    return total # units are in seconds * value units

  def get_windows_with_lowest_sum(self, earliest_start_time: datetime, latest_start_time: datetime, window_size: timedelta, resolution: timedelta) -> list[WindowWithLowestSumResult]:
    if earliest_start_time >= latest_start_time:
      return []
    
    windows: list[WindowWithLowestSumResult] = []

    current_time = earliest_start_time
    while current_time <= latest_start_time:
      until_time = current_time + window_size
      if until_time > self.get_last_time():
        break

      window_sum = self.get_window_sum(current_time, until_time)
      windows.append(WindowWithLowestSumResult(current_time, window_sum))

      current_time += resolution

    windows.sort(key=lambda x: x.sum_value)
    return windows