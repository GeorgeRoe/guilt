from guilt.dependencies.injector import DependencyInjector

from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.services.carbon_intensity_forecast import CarbonIntensityForecastService

from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.services.ip_info import IpInfoService

from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.services.plotting.plotext import PlotextPlottingService
from guilt.services.plotting.matplotlib import MatplotlibPlottingService

from guilt.interfaces.services.user import UserServiceInterface
from guilt.services.pwd_user import PwdUserService

from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.services.json_repository_factory import JsonRepositoryFactoryService

from guilt.interfaces.strategies.repository_setup import RepositorySetupStrategyInterface
from guilt.strategies.json_repository_setup import JsonRepositorySetupStrategy

import os

def bind_default_services(di: DependencyInjector) -> None:
  di.bind(CarbonIntensityForecastServiceInterface, CarbonIntensityForecastService)
  di.bind(IpInfoServiceInterface, IpInfoService)
  di.bind(UserServiceInterface, PwdUserService)

  # when a different storage method is used (e.g., sqlite), this should be changed
  di.bind(RepositoryFactoryServiceInterface, JsonRepositoryFactoryService)
  di.bind(RepositorySetupStrategyInterface, JsonRepositorySetupStrategy)

  di.bind(PlottingServiceInterface, MatplotlibPlottingService if os.getenv("TERM") == "xterm-kitty" else PlotextPlottingService)