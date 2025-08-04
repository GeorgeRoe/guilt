from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.utility.time_series_data import TimeSeriesData
from matplotlib import pyplot # type: ignore[import-untyped]
from matplotlib.dates import DateFormatter # type: ignore[import-untyped]
from pathlib import Path
import subprocess
import os

_temp_plot_name = ".temp_guilt_plot.png"

class MatplotlibPlottingService(PlottingServiceInterface):
  def __init__(self, user_service: UserServiceInterface) -> None:
    self.user_service = user_service

  def show(self) -> None:
    current_user = self.user_service.get_current_user()

    if current_user:
      temp_path = current_user.home_directory / _temp_plot_name
    else:
      temp_path = Path(os.getcwd()) / _temp_plot_name

    pyplot.savefig(temp_path)

    try:
      subprocess.run(["kitty", "+kitten", "icat", str(temp_path)], check=True)
    except subprocess.CalledProcessError:
      print("Failed to display the plot in kitty terminal. Please check if kitty is installed and configured correctly.")
    finally:
      os.remove(str(temp_path))

  def clear(self) -> None:
    pyplot.clf()

  def plot_time_series_data(self, data, title, xlabel, ylabel):
    values = [data.get_value_at(time) for time in data.get_times()]
    pyplot.plot(data.get_times(), values)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.title(title)

    pyplot.gcf().autofmt_xdate()
    pyplot.gca().xaxis.set_major_formatter(formatter = DateFormatter("%d/%m/%Y %H:%M"))

  def plot_horizontal_bar_data(self, data, title):
    pyplot.barh(list(data.keys()), list(data.values()))
    pyplot.title(title)