use super::{CarbonIntensityTimeSegment, FetchCarbonIntensity};
use chrono::{DateTime, Duration, Utc};
use std::collections::HashMap;
use anyhow;

pub struct CarbonIntensityAggregator<F: FetchCarbonIntensity> {
    postcode: String,
    segments: Vec<CarbonIntensityTimeSegment>,
    fetcher: F,
}

impl<F: FetchCarbonIntensity> CarbonIntensityAggregator<F> {
    pub fn new(postcode: String, fetcher: F) -> Self {
        Self {
            postcode,
            segments: Vec::new(),
            fetcher,
        }
    }

    pub async fn get_segments(
        &mut self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error> {
        let mut expected_start = from;
        let mut missing_ranges = Vec::new();

        while expected_start < to {
            let exists = self
                .segments
                .binary_search_by_key(&expected_start, |segment| segment.from)
                .is_ok();
            if exists {
                expected_start += Duration::minutes(30);
            } else {
                let start_missing = expected_start;

                while expected_start < to
                    && self
                        .segments
                        .binary_search_by_key(&expected_start, |segment| segment.from)
                        .is_err()
                {
                    expected_start += Duration::minutes(30);
                }
                missing_ranges.push((start_missing, expected_start));
            }
        }

        for (mut start, end) in missing_ranges {
            while start < end {
                let chunk_end = std::cmp::min(start + Duration::days(1), end);
                let new_segments = self.fetcher.fetch(start, chunk_end, &self.postcode).await?;
                self.segments.extend(new_segments);
                start = chunk_end;
            }
        }

        self.segments.sort_by_key(|segment| segment.from);
        self.segments
            .dedup_by(|a, b| a.from == b.from && a.to == b.to);

        let start = self
            .segments
            .iter()
            .position(|segment| segment.to > from)
            .unwrap_or(0);
        let end = self
            .segments
            .iter()
            .rposition(|segment| segment.from < to)
            .map(|i| i + 1)
            .unwrap_or(0);

        Ok(self.segments[start..end].to_vec())
    }

    pub async fn get_average_intensity(
        &mut self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Result<f64, anyhow::Error> {
        let segments = self.get_segments(from, to).await?;
        if segments.is_empty() {
            return Ok(0.0);
        }

        let mut total_intensity = 0.0;
        let mut total_time = 0.0;

        for segment in segments {
            let duration = (segment.to - segment.from).num_seconds() as f64;
            total_intensity += segment.intensity as f64 * duration;
            total_time += duration;
        }

        if total_time == 0.0 {
            return Ok(0.0);
        }

        Ok(total_intensity / total_time)
    }

    pub async fn get_average_generation_mix(
        &mut self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Result<HashMap<String, f64>, anyhow::Error> {
        let segments = self.get_segments(from, to).await?;
        if segments.is_empty() {
            return Ok(HashMap::new());
        }

        let mut total_mix: HashMap<String, f64> = HashMap::new();
        let mut total_time = 0.0;

        for segment in segments {
            let duration = (segment.to - segment.from).num_seconds() as f64;
            total_time += duration;

            for (source, percentage) in &segment.generation_mix {
                *total_mix.entry(source.clone()).or_insert(0.0) += percentage * duration;
            }
        }

        if total_time == 0.0 {
            return Ok(total_mix);
        }

        for value in total_mix.values_mut() {
            *value /= total_time;
        }

        Ok(total_mix)
    }
}
