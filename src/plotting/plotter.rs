use crate::carbon_intensity_api::CarbonIntensityTimeSegment;
use std::collections::HashMap;

pub trait Plotter {
    fn draw_generation_mix(&self, generation_mix: HashMap<String, f64>) -> anyhow::Result<()>;
    fn draw_intensity_forecast(
        &self,
        intensity_forecast: Vec<CarbonIntensityTimeSegment>,
    ) -> anyhow::Result<()>;
}
