use super::types::Data;
use super::{CarbonIntensityTimeSegment, DATE_TIME_FORMAT};
use chrono::{NaiveDateTime, ParseError, TimeZone, Utc};
use std::result::Result;

pub fn parse_api_data(data: Data) -> Result<CarbonIntensityTimeSegment, ParseError> {
    Ok(CarbonIntensityTimeSegment {
        from: Utc.from_utc_datetime(&NaiveDateTime::parse_from_str(
            &data.from,
            DATE_TIME_FORMAT,
        )?),
        to: Utc.from_utc_datetime(&NaiveDateTime::parse_from_str(&data.to, DATE_TIME_FORMAT)?),
        intensity: data.intensity.forecast,
        generation_mix: data
            .generationmix
            .iter()
            .map(|mix| (mix.fuel.clone(), mix.perc))
            .collect(),
    })
}
