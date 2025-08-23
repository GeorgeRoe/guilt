use super::types::SlurmBatchTest;
use regex::Regex;
use chrono::{DateTime, Local, NaiveDateTime, TimeZone, Utc};
use thiserror::Error;
use std::num::ParseIntError;
use chrono::ParseError;

#[derive(Debug, Error)]
pub enum SlurmBatchParsingError {
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
    pub fn from_line(line: &str) -> Result<Self, SlurmBatchParsingError> {
        let pattern = Regex::new(
            r"sbatch: Job (\d+) to start at ([\d\-T:]+) using (\d+) processors on nodes (.*?) in partition (\w+)"
        )?;

        let caps = pattern.captures(line)
            .ok_or_else(|| SlurmBatchParsingError::Format(line.to_string()))?;

        let job_id = caps.get(1).unwrap().as_str().to_string();
        let start_time_str = caps.get(2).unwrap().as_str();
        let processor_count_str = caps.get(3).unwrap().as_str();
        let nodes = caps.get(4).unwrap().as_str().to_string();
        let partition = caps.get(5).unwrap().as_str().to_string();

        let naive_dt = NaiveDateTime::parse_from_str(start_time_str, "%Y-%m-%dT%H:%M:%S")?;

        let local_dt = Local.from_local_datetime(&naive_dt)
            .single()
            .ok_or(SlurmBatchParsingError::Format("Ambiguous or non-existent local time".to_string()))?;

        let start_time: DateTime<Utc> = local_dt.with_timezone(&Utc);

        Ok(SlurmBatchTest {
            job_id,
            start_time,
            processor_count: processor_count_str.parse::<i32>()?,
            nodes,
            partition,
        })
    }
}