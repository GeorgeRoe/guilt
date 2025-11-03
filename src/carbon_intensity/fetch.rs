use super::CarbonIntensityTimeSegment;
use chrono::{DateTime, Utc};
use anyhow;
use async_trait::async_trait;

#[async_trait]
pub trait FetchCarbonIntensity {
    async fn fetch(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        postcode: &str,
    ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error>;
}