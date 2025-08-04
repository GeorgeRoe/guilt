from abc import ABC, abstractmethod
from guilt.utility.time_series_data import TimeSeriesData

class PlottingServiceInterface(ABC):
  @abstractmethod
  def show(self) -> None:
    pass

  @abstractmethod
  def clear(self) -> None:
    pass

  @abstractmethod
  def plot_time_series_data(self, data: TimeSeriesData, title: str, xlabel: str, ylabel: str) -> None:
    pass

  @abstractmethod
  def plot_horizontal_bar_data(self, data: dict[str, float], title: str) -> None:
    pass