use super::types::SlurmBatchTest;
use chrono::ParseError;
use chrono::{DateTime, Local, NaiveDateTime, TimeZone, Utc};
use regex::Regex;
use std::num::ParseIntError;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SlurmBatchTestParsingError {
    #[error("Failed to parse Slurm batch test line: {0}")]
    Regex(#[from] regex::Error),

    #[error("Incorrect format: {0}")]
    Format(String),

    #[error("Integer parsing error: {0}")]
    IntParse(#[from] ParseIntError),

    #[error("DateTime parsing error: {0}")]
    DateTimeParse(#[from] ParseError),
}

impl SlurmBatchTest {
    pub fn from_line(line: &str) -> Result<Self, SlurmBatchTestParsingError> {
        let pattern = Regex::new(
            r"sbatch: Job (\d+) to start at ([\d\-T:]+) using (\d+) processors on nodes (.*?) in partition (\w+)",
        )?;

        let caps = pattern
            .captures(line)
            .ok_or_else(|| SlurmBatchTestParsingError::Format(line.to_string()))?;

        if caps.len() != 6 {
            return Err(SlurmBatchTestParsingError::Format(line.to_string()));
        }

        let job_id = caps.get(1).unwrap().as_str().to_string();
        let start_time_str = caps.get(2).unwrap().as_str();
        let processor_count_str = caps.get(3).unwrap().as_str();
        let nodes = caps.get(4).unwrap().as_str().to_string();
        let partition = caps.get(5).unwrap().as_str().to_string();

        let naive_dt = NaiveDateTime::parse_from_str(start_time_str, "%Y-%m-%dT%H:%M:%S")
            .map_err(SlurmBatchTestParsingError::DateTimeParse)?;

        let local_dt = Local.from_local_datetime(&naive_dt).single().ok_or(
            SlurmBatchTestParsingError::Format("Ambiguous or non-existent local time".to_string()),
        )?;

        let start_time: DateTime<Utc> = local_dt.with_timezone(&Utc);

        let processor_count = processor_count_str
            .parse::<i32>()
            .map_err(SlurmBatchTestParsingError::IntParse)?;

        Ok(SlurmBatchTest {
            job_id,
            start_time,
            processor_count,
            nodes,
            partition,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_string() {
        let line = "sbatch: Job 100 to start at 2026-01-01T12:00:00 using 2 processors on nodes cn045 in partition partition1";

        let result = SlurmBatchTest::from_line(line).unwrap();

        assert_eq!(result.job_id, "100");
        assert_eq!(
            result.start_time,
            Utc.with_ymd_and_hms(2026, 1, 1, 12, 0, 0).unwrap()
        );
        assert_eq!(result.processor_count, 2);
        assert_eq!(result.nodes, "cn045");
        assert_eq!(result.partition, "partition1");
    }

    #[test]
    fn test_invalid_string() {
        let line = "invalid sbatch output string";

        let result = SlurmBatchTest::from_line(line);

        assert!(result.is_err());
    }

    #[test]
    fn test_invalid_datetime() {
        let line = "sbatch: Job 100 to start at 2026-13-32T25:61:61 using 2 processors on nodes cn045 in partition partition1";

        let result = SlurmBatchTest::from_line(line);

        assert!(
            matches!(result, Err(SlurmBatchTestParsingError::DateTimeParse(_))),
            "Expected DateTimeParse error, but got {:?}",
            result
        );
    }
}
