use super::api_types::{ApiError, RegionData};
use super::DATE_TIME_FORMAT;
use crate::carbon_intensity_api::CarbonIntensityTimeSegment;
use chrono::{DateTime, Utc};
use reqwest;
use std::result::Result;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CarbonIntensityApiFetchError {
    #[error("API error: {0}")]
    Request(#[from] reqwest::Error),

    #[error("Deserialization error: {0}")]
    Parse(#[from] serde_json::Error),

    #[error("Date parsing error: {0}")]
    DateParse(#[from] chrono::ParseError),

    #[error("Api Error: (code: {0}) {1}")]
    ApiError(String, String),

    #[error("Unexpected response format")]
    UnexpectedResponseFormat,
}

pub async fn fetch_carbon_intensity(
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

    println!("Fetching carbon intensity data from: {}", url);

    let response = reqwest::get(&url).await?;

    let response = response.error_for_status()?;

    let json = response.json::<serde_json::Value>().await?;

    if let Some(data) = json.get("data") {
        let data: RegionData = serde_json::from_value(data.clone())?;

        println!("successful response: {:?}", data);

        Ok(data
            .data
            .into_iter()
            .map(CarbonIntensityTimeSegment::from_api_data)
            .collect::<Result<Vec<_>, _>>()?)
    } else if let Some(error) = json.get("error") {
        let api_error: ApiError = serde_json::from_value(error.clone())?;

        Err(CarbonIntensityApiFetchError::ApiError(
            api_error.code,
            api_error.message,
        ))
    } else {
        Err(CarbonIntensityApiFetchError::UnexpectedResponseFormat)
    }
}
