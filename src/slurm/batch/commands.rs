use super::parsing::SlurmBatchTestParsingError;
use super::types::SlurmBatchTest;
use crate::safe_command::{SafeCommandError, safe_get_stderr, safe_get_stdout};
use chrono::NaiveDateTime;
use std::process::Command;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SlurmBatchCommandError {
    #[error("Failed to execute Slurm batch command: {0}")]
    SafeCommand(#[from] SafeCommandError),

    #[error("Failed to parse slurm batch output: {0}")]
    Parsing(#[from] SlurmBatchTestParsingError),
}

pub fn test(
    file: &str,
    begin: Option<NaiveDateTime>,
) -> Result<SlurmBatchTest, SlurmBatchCommandError> {
    let mut args: Vec<String> = vec!["--test-only".to_string()];

    if let Some(begin_time) = begin {
        let begin_str = begin_time.format("%Y-%m-%dT%H:%M:%S").to_string();
        args.push("--begin".to_string());
        args.push(begin_str);
    }

    args.push(file.to_string());

    let output = Command::new("sbatch").args(&args).output();

    let stderr = safe_get_stderr(output)?;

    Ok(SlurmBatchTest::from_line(&stderr)?)
}

pub fn submit(file: &str, begin: Option<NaiveDateTime>) -> Result<String, SlurmBatchCommandError> {
    let mut args: Vec<String> = vec!["--parsable".to_string()];

    if let Some(begin_time) = begin {
        let begin_str = begin_time.format("%Y-%m-%dT%H:%M:%S").to_string();
        args.push("--begin".to_string());
        args.push(begin_str);
    }

    args.push(file.to_string());

    let output = Command::new("sbatch").args(&args).output();

    let stdout = safe_get_stdout(output)?;

    Ok(stdout.trim().to_string())
}
