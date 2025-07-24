from guilt.mappers.carbon_intensity_forecast_result import MapToCarbonIntensityForecastResult
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.mappers.cpu_profiles_config import MapToCpuProfilesConfig
from guilt.mappers.get_entries_password_result import MapToGetEntriesPasswordResult
from guilt.mappers.guilt_script_directives import MapToGuiltScriptDirectives
from guilt.mappers.ip_info_result import MapToIpInfoResult
from guilt.mappers.json import MapToJson
from guilt.mappers.processed_jobs_data import MapToProcessedJobsData
from guilt.mappers.slurm_accounting_result import MapToSlurmAccountingResult
from guilt.mappers.slurm_script_directives import MapToSlurmScriptDirectives
from guilt.mappers.unprocessed_job import MapToUnprocessedJob
from guilt.mappers.unprocessed_jobs_data import MapToUnprocessedJobsData
from dataclasses import dataclass

@dataclass
class MapperRegistry:
  carbon_intensity_forecast_result: MapToCarbonIntensityForecastResult = MapToCarbonIntensityForecastResult()
  carbon_intensity_time_segment: MapToCarbonIntensityTimeSegment = MapToCarbonIntensityTimeSegment()
  cpu_profile: MapToCpuProfile = MapToCpuProfile()
  cpu_profiles_config: MapToCpuProfilesConfig = MapToCpuProfilesConfig()
  get_entries_password_result: MapToGetEntriesPasswordResult = MapToGetEntriesPasswordResult()
  guilt_script_directives: MapToGuiltScriptDirectives = MapToGuiltScriptDirectives()
  ip_info_result: MapToIpInfoResult = MapToIpInfoResult()
  json: MapToJson = MapToJson()
  processed_jobs_data: MapToProcessedJobsData = MapToProcessedJobsData()
  slurm_accounting_result: MapToSlurmAccountingResult = MapToSlurmAccountingResult()
  slurm_script_directives: MapToSlurmScriptDirectives = MapToSlurmScriptDirectives()
  unprocessed_job: MapToUnprocessedJob = MapToUnprocessedJob()
  unprocessed_jobs_data: MapToUnprocessedJobsData = MapToUnprocessedJobsData()