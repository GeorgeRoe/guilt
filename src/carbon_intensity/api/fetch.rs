use super::{
    CarbonIntensityTimeSegment, DATE_TIME_FORMAT, FetchCarbonIntensity,
    parsing::parse_api_data,
    types::{ApiError, RegionData},
};
use async_trait::async_trait;
use chrono::{DateTime, Utc};
use reqwest;
use std::result::Result;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CarbonIntensityApiParseError {
    #[error("Deserialization error: {0}")]
    Parse(#[from] serde_json::Error),

    #[error("Date parsing error: {0}")]
    DateParse(#[from] chrono::ParseError),

    #[error("Api Error: (code: {0}) {1}")]
    ApiError(String, String),

    #[error("Unexpected response format")]
    UnexpectedResponseFormat,
}

#[derive(Error, Debug)]
pub enum CarbonIntensityApiFetchError {
    #[error("API error: {0}")]
    Request(#[from] reqwest::Error),

    #[error("Parsing error: {0}")]
    Parse(#[from] CarbonIntensityApiParseError),
}

fn parse_json_response(
    json: serde_json::Value,
) -> Result<Vec<CarbonIntensityTimeSegment>, CarbonIntensityApiParseError> {
    println!("Parsing JSON response: {:?}\n", json);
    match (json.get("data"), json.get("error")) {
        (Some(data), None) => {
            println!("Data found in JSON response: {:?}", data);
            let data: RegionData = serde_json::from_value(data.to_owned())?;
            let segments = data
                .data
                .into_iter()
                .map(parse_api_data)
                .collect::<Result<Vec<_>, _>>()?;
            Ok(segments)
        }
        (None, Some(error)) => {
            let error: ApiError = serde_json::from_value(error.to_owned())?;
            Err(CarbonIntensityApiParseError::ApiError(
                error.code,
                error.message,
            ))
        }
        _ => Err(CarbonIntensityApiParseError::UnexpectedResponseFormat),
    }
}

async fn api_fetch_carbon_intensity(
    from: DateTime<Utc>,
    to: DateTime<Utc>,
    postcode: &str,
) -> Result<Vec<CarbonIntensityTimeSegment>, CarbonIntensityApiFetchError> {
    let url = format!(
        "https://api.carbonintensity.org.uk/regional/intensity/{}/{}/postcode/{}",
        from.format(DATE_TIME_FORMAT),
        to.format(DATE_TIME_FORMAT),
        postcode
    );

    let response = reqwest::get(&url).await?.error_for_status()?;

    let json = response.json::<serde_json::Value>().await?;

    Ok(parse_json_response(json)?)
}

pub struct ApiFetchCarbonIntensity {
    postcode: String,
}

impl ApiFetchCarbonIntensity {
    pub fn new(postcode: String) -> Self {
        Self { postcode }
    }
}

#[async_trait]
impl FetchCarbonIntensity for ApiFetchCarbonIntensity {
    async fn fetch(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error> {
        api_fetch_carbon_intensity(from, to, &self.postcode)
            .await
            .map_err(anyhow::Error::from)
    }
}

#[cfg(test)]
mod tests {
    use super::{parse_json_response, CarbonIntensityApiParseError};
    use chrono::{TimeZone, Utc};

    fn sample_success() -> serde_json::Value {
        serde_json::json!({
            "data": {
                "data": [
                    {
                        "from": "2024-01-01T00:00Z",
                        "to": "2024-01-01T01:00Z",
                        "intensity": {
                            "forecast": 266
                        },
                        "generationmix": [
                            {"fuel": "gas", "perc": 43.6},
                            {"fuel": "solar", "perc": 18.1},
                            {"fuel": "coal", "perc": 0.7},
                            {"fuel": "nuclear", "perc": 17.6},
                            {"fuel": "wind", "perc": 6.8},
                            {"fuel": "hydro", "perc": 2.2},
                            {"fuel": "biomass", "perc": 5.0},
                            {"fuel": "imports", "perc": 5.0},
                            {"fuel": "other", "perc": 0.0}
                        ]
                    }
                ]
            }
        })
    }

    fn sample_failure() -> serde_json::Value {
        serde_json::json!({
            "error": {
                "code": "400 Bad Request",
                "message": "Invalid postcode"
            }
        })
    }

    fn sample_unexpected() -> serde_json::Value {
        serde_json::json!({
            "data": "exists",
            "error": "also exists",
        })
    }

    #[test]
    fn test_parse_json_response_success() {
        let json = sample_success();
        let result = parse_json_response(json);
        match result {
            Ok(segments) => {
                match segments.first() {
                    Some(segment) => {
                        assert_eq!(segment.from, Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap());
                        assert_eq!(segment.to, Utc.with_ymd_and_hms(2024, 1, 1, 1, 0, 0).unwrap());

                        assert_eq!(segment.intensity, 266);

                        assert_eq!(segment.generation_mix.len(), 9);
                        assert_eq!(segment.generation_mix.get("gas"), Some(&43.6));
                        assert_eq!(segment.generation_mix.get("solar"), Some(&18.1));
                        assert_eq!(segment.generation_mix.get("coal"), Some(&0.7));
                        assert_eq!(segment.generation_mix.get("nuclear"), Some(&17.6));
                        assert_eq!(segment.generation_mix.get("wind"), Some(&6.8));
                        assert_eq!(segment.generation_mix.get("hydro"), Some(&2.2));
                    }
                    None => panic!("Expected at least one segment"),
                }
            },
            Err(error) => panic!("Expected success, got error: {}", error),
        }
    }

    #[test]
    fn test_parse_json_response_failure() {
        let json = sample_failure();
        let result = parse_json_response(json);
        match result {
            Ok(_) => panic!("Expected error, got success"),
            Err(error) => match error {
                CarbonIntensityApiParseError::ApiError(code, message) => {
                    assert_eq!(code, "400 Bad Request");
                    assert_eq!(message, "Invalid postcode");
                },
                _ => panic!("Expected ApiError, got different error"),
            },
        }
    }

    #[test]
    fn test_parse_json_response_unexpected_format() {
        let json = sample_unexpected();
        let result = parse_json_response(json);
        match result {
            Ok(_) => panic!("Expected error, got success"),
            Err(error) => match error {
                CarbonIntensityApiParseError::UnexpectedResponseFormat => {},
                _ => panic!("Expected UnexpectedResponseFormat, got different error"),
            },
        }
    }
}
