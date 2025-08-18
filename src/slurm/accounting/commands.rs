use super::parsing::parse_command_output;
use super::types::SlurmAccountingResult;
use crate::safe_command::{SafeCommandError, safe_get_stdout};
use crate::structured_json::errors::StructuredJsonParsingError;
use std::process::Command;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SlurmAccountingCommandError {
    #[error("Failed to execute Slurm accounting command: {0}")]
    SafeCommand(#[from] SafeCommandError),

    #[error("Failed to parse Slurm accounting JSON output: {0}")]
    Json(#[from] StructuredJsonParsingError),
}

pub fn get_all_historical_jobs_for_user(
    user: &str,
) -> Result<Vec<SlurmAccountingResult>, SlurmAccountingCommandError> {
    let output = Command::new("sacct")
        .arg("--user")
        .arg(user)
        .arg("--starttime")
        .arg("1970-01-01")
        .arg("--json")
        .output();

    let stdout = safe_get_stdout(output).map_err(SlurmAccountingCommandError::SafeCommand)?;

    parse_command_output(&stdout).map_err(SlurmAccountingCommandError::Json)
}

pub fn get_jobs_by_id(
    job_ids: &[String],
) -> Result<Vec<SlurmAccountingResult>, SlurmAccountingCommandError> {
    let output = Command::new("sacct")
        .arg("--jobs")
        .arg(job_ids.join(","))
        .arg("--json")
        .output();

    let stdout = safe_get_stdout(output).map_err(SlurmAccountingCommandError::SafeCommand)?;

    parse_command_output(&stdout).map_err(SlurmAccountingCommandError::Json)
}
