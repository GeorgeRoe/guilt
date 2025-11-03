use crate::carbon_intensity::CarbonIntensityTimeSegment;
use std::collections::HashMap;

pub type GenerationMixData = HashMap<String, f64>;
pub type CarbonIntensityForecastData = Vec<CarbonIntensityTimeSegment>;

pub enum ChartDefinition {
    GenerationMix(GenerationMixData),
    CarbonIntensityForecast(CarbonIntensityForecastData),
}
