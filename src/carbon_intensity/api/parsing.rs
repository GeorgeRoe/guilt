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

#[cfg(test)]
mod tests {
    use super::{
        super::types::{Data, GenerationMix, Intensity},
        parse_api_data,
    };
    use chrono::{TimeZone, Utc};

    #[test]
    fn test_parse_api_data() {
        let data = Data {
            from: "2025-01-01T00:00Z".to_string(),
            to: "2025-01-01T01:00Z".to_string(),
            intensity: Intensity { forecast: 150 },
            generationmix: vec![
                GenerationMix {
                    fuel: "coal".to_string(),
                    perc: 40.0,
                },
                GenerationMix {
                    fuel: "wind".to_string(),
                    perc: 60.0,
                },
            ],
        };

        let result = parse_api_data(data).unwrap();

        assert_eq!(
            result.from,
            Utc.with_ymd_and_hms(2025, 1, 1, 0, 0, 0).unwrap()
        );
        assert_eq!(
            result.to,
            Utc.with_ymd_and_hms(2025, 1, 1, 1, 0, 0).unwrap()
        );
        assert_eq!(result.intensity, 150);
        assert_eq!(result.generation_mix.get("coal"), Some(&40.0));
        assert_eq!(result.generation_mix.get("wind"), Some(&60.0));
    }
}
