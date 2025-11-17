use super::{CarbonIntensityTimeSegment, FetchCarbonIntensity};
use anyhow;
use chrono::{DateTime, Duration, Utc};
use std::collections::HashMap;

pub struct CarbonIntensityAggregator<F: FetchCarbonIntensity> {
    segments: Vec<CarbonIntensityTimeSegment>,
    fetcher: F,
}

impl<F: FetchCarbonIntensity> CarbonIntensityAggregator<F> {
    pub fn new(fetcher: F) -> Self {
        Self {
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
                let new_segments = self.fetcher.fetch(start, chunk_end).await?;
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

#[cfg(test)]
mod tests {
    use super::{CarbonIntensityTimeSegment, FetchCarbonIntensity, CarbonIntensityAggregator};
    use async_trait::async_trait;
    use chrono::{DateTime, Duration, TimeZone, Timelike, Utc};
    use tokio;
    use std::collections::HashMap;

    fn floor_to_half_hour(dt: DateTime<Utc>) -> DateTime<Utc> {
        let minute = if dt.minute() < 30 { 0 } else { 30 };
        let naive = dt.naive_local()
            .with_minute(minute).unwrap()
            .with_second(0).unwrap()
            .with_nanosecond(0).unwrap();
        Utc.from_local_datetime(&naive).unwrap()
    }

    #[test]
    fn test_floor_to_half_hour() {
        let dt = Utc.with_ymd_and_hms(2024, 1, 1, 10, 45, 0).unwrap();
        let floored = floor_to_half_hour(dt);
        assert_eq!(floored, Utc.with_ymd_and_hms(2024, 1, 1, 10, 30, 0).unwrap());
    }

    struct MockFetchCarbonIntensity {
        intensity: i32,
        generation_mix: HashMap<String, f64>,
    }

    impl MockFetchCarbonIntensity {
        fn new(intensity: i32, generation_mix: HashMap<String, f64>) -> Self {
            Self {
                intensity,
                generation_mix,
            }
        }
    }

    #[async_trait]
    impl FetchCarbonIntensity for MockFetchCarbonIntensity {
        async fn fetch(
            &self,
            from: DateTime<Utc>,
            to: DateTime<Utc>,
        ) -> Result<Vec<CarbonIntensityTimeSegment>, anyhow::Error> {
            let mut segments = Vec::new();
            let mut current = floor_to_half_hour(from);
            while current < to {
                segments.push(CarbonIntensityTimeSegment {
                    from: current,
                    to: current + Duration::minutes(30),
                    intensity: self.intensity,
                    generation_mix: self.generation_mix.clone(),
                });
                current += Duration::minutes(30);
            }
            Ok(segments)
        }
    }

    #[tokio::test]
    async fn test_mock_fetch() {
        let fetcher = MockFetchCarbonIntensity::new(100, HashMap::new());
        let result = fetcher.fetch(
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 10, 0).unwrap(),
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 20, 0).unwrap(),
        ).await;

        match result {
            Ok(segments) => {
                assert_eq!(segments.len(), 1);
                match segments.first() {
                    Some(segment) => {
                        assert_eq!(segment.from, Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap());
                        assert_eq!(segment.to, Utc.with_ymd_and_hms(2024, 1, 1, 0, 30, 0).unwrap());
                        assert_eq!(segment.intensity, 100.0 as i32);
                        assert_eq!(segment.generation_mix.len(), 0);
                    }
                    None => {
                        panic!("No segments returned");
                    }
                }
            },
            Err(e) => {
                panic!("Fetch failed: {:?}", e);
            }
        }
    }

    #[tokio::test]
    async fn test_aggregator_get_segments() {
        let fetcher = MockFetchCarbonIntensity::new(100, HashMap::new());
        let mut aggregator = CarbonIntensityAggregator::new(fetcher);
        let result = aggregator.get_segments(
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 10, 0).unwrap(),
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 20, 0).unwrap(),
        ).await;

        match result {
            Ok(segments) => {
                assert_eq!(segments.len(), 1);
                match segments.first() {
                    Some(segment) => {
                        assert_eq!(segment.from, Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap());
                        assert_eq!(segment.to, Utc.with_ymd_and_hms(2024, 1, 1, 0, 30, 0).unwrap());
                        assert_eq!(segment.intensity, 100.0 as i32);
                        assert_eq!(segment.generation_mix.len(), 0);

                    }, None => {
                        panic!("No segments returned");
                    }
                }
            },
            Err(e) => {
                panic!("Aggregator get_segments failed: {:?}", e);
            }
        }
    }

    #[tokio::test]
    async fn test_aggregator_get_average_intensity() {
        let fetcher = MockFetchCarbonIntensity::new(100, HashMap::new());
        let mut aggregator = CarbonIntensityAggregator::new(fetcher);
        let result = aggregator.get_average_intensity(
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap(),
            Utc.with_ymd_and_hms(2024, 1, 1, 1, 0, 0).unwrap(),
        ).await;

        match result {
            Ok(avg_intensity) => {
                assert_eq!(avg_intensity, 100.0);
            },
            Err(e) => {
                panic!("Aggregator get_average_intensity failed: {:?}", e);
            }
        }
    }

    #[tokio::test]
    async fn test_aggregator_get_average_generation_mix() {
        let fetcher = MockFetchCarbonIntensity::new(100, {
            let mut mix = HashMap::new();
            mix.insert("solar".to_string(), 50.0);
            mix.insert("wind".to_string(), 50.0);
            mix
        });
        let mut aggregator = CarbonIntensityAggregator::new(fetcher);
        let result = aggregator.get_average_generation_mix(
            Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap(),
            Utc.with_ymd_and_hms(2024, 1, 1, 1, 0, 0).unwrap(),
        ).await;

        match result {
            Ok(avg_mix) => {
                assert_eq!(avg_mix.len(), 2);
                assert_eq!(*avg_mix.get("solar").unwrap(), 50.0);
                assert_eq!(*avg_mix.get("wind").unwrap(), 50.0);
            },
            Err(e) => {
                panic!("Aggregator get_average_generation_mix failed: {:?}", e);
            }
        }
    }
}