use super::{GuiltScriptDirectives, SlurmScriptDirectives};
use crate::parse_duration_string;
use std::collections::HashMap;
use thiserror::Error;

enum StringOrPresent {
    Str(String),
    Present,
}

fn parse_directive_lines(
    directive_prefix: &str,
    lines: Vec<String>,
) -> HashMap<String, StringOrPresent> {
    lines
        .iter()
        .filter_map(|line| line.strip_prefix(directive_prefix))
        .filter_map(|line| line.strip_prefix(" --"))
        .filter_map(|line| {
            let trimmed = line.trim();

            if trimmed.is_empty() {
                None
            } else if !trimmed.contains("=") {
                Some((trimmed.to_string(), StringOrPresent::Present))
            } else if let Some((key, value)) = trimmed.split_once("=") {
                Some((key.to_string(), StringOrPresent::Str(value.to_string())))
            } else {
                None
            }
        })
        .collect()
}

#[derive(Debug, Error)]
pub enum GuiltScriptDirectivesParsingError {
    #[error("Missing required cpu-profile directive")]
    MissingCpuProfile,
}

impl GuiltScriptDirectives {
    pub fn from_file_contents(contents: &str) -> Result<Self, GuiltScriptDirectivesParsingError> {
        let directives = parse_directive_lines(
            "#GUILT",
            contents.lines().map(|line| line.to_string()).collect(),
        );

        let cpu_profile = match directives.get("cpu-profile") {
            Some(StringOrPresent::Str(s)) => s.clone(),
            Some(StringOrPresent::Present) => {
                return Err(GuiltScriptDirectivesParsingError::MissingCpuProfile);
            }
            None => return Err(GuiltScriptDirectivesParsingError::MissingCpuProfile),
        };

        Ok(Self { cpu_profile })
    }
}

#[derive(Debug, Error)]
pub enum SlurmScriptDirectivesParsingError {
    #[error("Missing required key in Slurm directives: {0}")]
    MissingKey(String),

    #[error("Unable to parse for key {0}: {1}")]
    ParseError(String, String),

    #[error("Unable to parse duration string for key {0}: {1}")]
    DurationParseError(String, String),
}

impl SlurmScriptDirectives {
    pub fn from_file_contents(contents: &str) -> Result<Self, SlurmScriptDirectivesParsingError> {
        let directives = parse_directive_lines(
            "#SBATCH",
            contents.lines().map(|line| line.to_string()).collect(),
        );

        let time_string = match directives.get("time") {
            Some(StringOrPresent::Str(s)) => s,
            _ => {
                return Err(SlurmScriptDirectivesParsingError::MissingKey(
                    "time".to_string(),
                ));
            }
        };

        let time = parse_duration_string(time_string).map_err(|e| {
            SlurmScriptDirectivesParsingError::DurationParseError("time".to_string(), e)
        })?;

        let nodes = match directives.get("nodes") {
            Some(StringOrPresent::Str(s)) => s.parse::<i32>().map_err(|e| {
                SlurmScriptDirectivesParsingError::ParseError("nodes".to_string(), e.to_string())
            })?,
            _ => {
                return Err(SlurmScriptDirectivesParsingError::MissingKey(
                    "nodes".to_string(),
                ));
            }
        };

        let tasks_per_node = match directives.get("tasks-per-node") {
            Some(StringOrPresent::Str(s)) => s.parse::<i32>().map_err(|e| {
                SlurmScriptDirectivesParsingError::ParseError(
                    "tasks-per-node".to_string(),
                    e.to_string(),
                )
            })?,
            _ => {
                return Err(SlurmScriptDirectivesParsingError::MissingKey(
                    "tasks-per-node".to_string(),
                ));
            }
        };

        let cpus_per_task = match directives.get("cpus-per-task") {
            Some(StringOrPresent::Str(s)) => s.parse::<i32>().map_err(|e| {
                SlurmScriptDirectivesParsingError::ParseError(
                    "cpus-per-task".to_string(),
                    e.to_string(),
                )
            })?,
            _ => {
                return Err(SlurmScriptDirectivesParsingError::MissingKey(
                    "cpus-per-task".to_string(),
                ));
            }
        };

        Ok(Self {
            time,
            nodes,
            tasks_per_node,
            cpus_per_task,
        })
    }
}
