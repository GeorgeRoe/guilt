use crate::carbon_intensity_api::CarbonIntensityTimeSegment;
use std::collections::HashMap;

pub type GenerationMixData = HashMap<String, f64>;
pub type CarbonIntensityForecastData = Vec<CarbonIntensityTimeSegment>;

pub enum ChartDefinition {
    GenerationMix(GenerationMixData),
    CarbonIntensityForecast(CarbonIntensityForecastData),
}