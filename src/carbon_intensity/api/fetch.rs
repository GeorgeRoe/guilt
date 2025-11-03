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

pub struct ApiFetchCarbonIntensity;

#[async_trait]
impl FetchCarbonIntensity for ApiFetchCarbonIntensity {
    async fn fetch(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        postcode: &str,
    ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error> {
        fetch_carbon_intensity_with_api(from, to, postcode)
            .await
            .map_err(anyhow::Error::from)
    }
}

pub async fn fetch_carbon_intensity_with_api(
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

    match (json.get("data"), json.get("error")) {
        (Some(data), Some(_)) => {
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
            Err(CarbonIntensityApiFetchError::ApiError(
                error.code,
                error.message,
            ))
        }
        _ => Err(CarbonIntensityApiFetchError::UnexpectedResponseFormat),
    }
}

mod tests {}
