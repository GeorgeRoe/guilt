use super::api_types::Data;
use super::{CarbonIntensityTimeSegment, DATE_TIME_FORMAT};
use chrono::{DateTime, ParseError, Utc};
use std::result::Result;

impl CarbonIntensityTimeSegment {
    pub fn from_api_data(data: Data) -> Result<Self, ParseError> {
        Ok(Self {
            from: DateTime::parse_from_str(&data.from, DATE_TIME_FORMAT)?.with_timezone(&Utc),
            to: DateTime::parse_from_str(&data.to, DATE_TIME_FORMAT)?.with_timezone(&Utc),
            intensity: data.intensity.forecast,
            generation_mix: data
                .generationmix
                .iter()
                .map(|mix| (mix.fuel.clone(), mix.perc))
                .collect(),
        })
    }
}
