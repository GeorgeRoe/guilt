from guilt.mappers.carbon_intensity_forecast_result import MapToCarbonIntensityForecastResult
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment
from guilt.mappers.guilt_script_directives import MapToGuiltScriptDirectives
from guilt.mappers.json import MapToJson
from guilt.mappers.slurm_batch_test_result import MapToSlurmBatchTestResult
from guilt.mappers.slurm_script_directives import MapToSlurmScriptDirectives
from guilt.mappers.time_series_data import MapToTimeSeriesData
from dataclasses import dataclass

@dataclass
class MapperRegistry:
  carbon_intensity_forecast_result: MapToCarbonIntensityForecastResult = MapToCarbonIntensityForecastResult()
  carbon_intensity_time_segment: MapToCarbonIntensityTimeSegment = MapToCarbonIntensityTimeSegment()
  guilt_script_directives: MapToGuiltScriptDirectives = MapToGuiltScriptDirectives()
  json: MapToJson = MapToJson()
  slurm_batch_test_result: MapToSlurmBatchTestResult = MapToSlurmBatchTestResult()
  slurm_script_directives: MapToSlurmScriptDirectives = MapToSlurmScriptDirectives()
  time_series_data: MapToTimeSeriesData = MapToTimeSeriesData()