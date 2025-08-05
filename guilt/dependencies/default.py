from guilt.dependencies.injector import DependencyInjector

from guilt.services.carbon_intensity_forecast import CarbonIntensityForecastService
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from guilt.services.ip_info import IpInfoService
from guilt.services.plotting.plotext import PlotextPlottingService
from guilt.services.plotting.matplotlib import MatplotlibPlottingService
from guilt.services.processed_jobs_data import ProcessedJobsDataService
from guilt.services.pwd_user import PwdUserService
from guilt.services.setup import SetupService
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService

from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.setup import SetupServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.user import UserServiceInterface

import os

def bind_default_services(di: DependencyInjector) -> None:
  di.bind(CarbonIntensityForecastServiceInterface, CarbonIntensityForecastService)
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  di.bind(IpInfoServiceInterface, IpInfoService)
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  di.bind(SetupServiceInterface, SetupService)
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  di.bind(UserServiceInterface, PwdUserService)

  di.bind(PlottingServiceInterface, MatplotlibPlottingService if os.getenv("TERM") == "xterm-kitty" else PlotextPlottingService)