use super::CarbonIntensityTimeSegment;
use anyhow;
use async_trait::async_trait;
use chrono::{DateTime, Utc};

#[async_trait]
pub trait FetchCarbonIntensity {
    async fn fetch(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error>;
}
