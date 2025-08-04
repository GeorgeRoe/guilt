from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.utility.time_series_data import TimeSeriesData
import plotext # type: ignore[import-untyped]
import shutil

class PlotextPlottingService(PlottingServiceInterface):
  def show(self) -> None:
    plotext.show()
    
  def clear(self) -> None:
    plotext.clear_figure()
  
  def plot_time_series_data(self, data: TimeSeriesData, title: str, xlabel: str, ylabel: str) -> None:
    columns, rows = shutil.get_terminal_size()
    width = columns - 1
    height = max(15, int(rows / 3))
    plotext.plot_size(width, height)
    plotext.theme("pro")
    plotext.date_form("d/m/Y H:M")

    values = [data.get_value_at(time) for time in data.get_times()]
    datetimes = plotext.datetimes_to_string(data.get_times())
    plotext.plot(datetimes, values, marker="braille")

    plotext.title(title)
    plotext.xlabel(xlabel)
    plotext.ylabel(ylabel)

  def plot_horizontal_bar_data(self, data: dict[str, float], title: str) -> None:
    columns, _ = shutil.get_terminal_size()

    plotext.simple_bar(
      list(data.keys()),
      list(data.values()),
      title = title,
      width = columns - 1
    )