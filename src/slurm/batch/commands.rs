use chrono::{NaiveDateTime};
use thiserror::Error;
use std::process::Command;
use crate::safe_command::{SafeCommandError, safe_get_stdout};
use super::types::SlurmBatchTest;
use super::parsing::SlurmBatchParsingError;

#[derive(Debug, Error)]
pub enum SlurmBatchCommandError {
    #[error("Failed to execute Slurm batch command: {0}")]
    SafeCommand(#[from] SafeCommandError),

    #[error("Failed to parse slurm batch output: {0}")]
    Parsing(#[from] SlurmBatchParsingError),
}

pub fn test(file: &str, begin: Option<NaiveDateTime>) -> Result<SlurmBatchTest, SlurmBatchCommandError> {
    let mut args: Vec<String> = vec!["--test-only".to_string()];

    if let Some(begin_time) = begin {
        let begin_str = begin_time.format("%Y-%m-%dT%H:%M:%S").to_string();
        args.push("--begin".to_string());
        args.push(begin_str);
    }

    args.push(file.to_string());

    let output = Command::new("sbatch")
        .args(&args)
        .output();

    let stdout = safe_get_stdout(output)?;

    Ok(SlurmBatchTest::from_line(&stdout)?)
}