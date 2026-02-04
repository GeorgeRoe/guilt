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
    let prefix = format!("{directive_prefix} --");
    lines
        .iter()
        .filter_map(|line| line.strip_prefix(prefix.as_str()))
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
            Some(StringOrPresent::Str(s)) => Some(s.clone()),
            Some(StringOrPresent::Present) => {
                Err(GuiltScriptDirectivesParsingError::MissingCpuProfile)?
            }
            _ => None,
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_guilt_script_directives_parsing() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile=AMD Epyc 7742
#SBATCH --time=01:30:00
#SBATCH --nodes=2
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=8
echo "Hello, World!"
"#;

        let guilt_directives = GuiltScriptDirectives::from_file_contents(script_contents).unwrap();

        assert!(matches!(
            guilt_directives.cpu_profile,
            Some(name) if name == "AMD Epyc 7742"
        ));
    }

    #[test]
    fn test_guilt_script_diretives_parsing_no_cpu_profile() {
        let script_contents = r#"#!/bin/bash
#SBATCH --time=01:30:00
#SBATCH --nodes=2
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=8
echo "Hello, World!"
"#;

        let guilt_directives = GuiltScriptDirectives::from_file_contents(script_contents).unwrap();

        assert!(matches!(guilt_directives.cpu_profile, None));
    }

    #[test]
    fn test_guilt_script_directives_parsing_missing_value() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile
#SBATCH --time=01:30:00
#SBATCH --nodes=2
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=8
echo "Hello, World!"
"#;

        let result = GuiltScriptDirectives::from_file_contents(script_contents);

        assert!(matches!(
            result,
            Err(GuiltScriptDirectivesParsingError::MissingCpuProfile)
        ));
    }

    #[test]
    fn test_guilt_script_directives_parsing_with_flag() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile
#SBATCH --time=01:30:00
#SBATCH --nodes=2
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=8
echo "Hello, World!"
"#;
        let result = GuiltScriptDirectives::from_file_contents(script_contents);

        assert!(matches!(
            result,
            Err(GuiltScriptDirectivesParsingError::MissingCpuProfile)
        ));
    }

    #[test]
    fn test_slurm_script_directives_parsing() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile=AMD Epyc 7742
#SBATCH --time=00:01:00
#SBATCH --nodes=3
#SBATCH --tasks-per-node=5
#SBATCH --cpus-per-task=10
echo "Hello, World!"
"#;

        let slurm_directives = SlurmScriptDirectives::from_file_contents(script_contents).unwrap();

        assert_eq!(slurm_directives.time.as_seconds_f32(), 60.0);
        assert_eq!(slurm_directives.nodes, 3);
        assert_eq!(slurm_directives.tasks_per_node, 5);
        assert_eq!(slurm_directives.cpus_per_task, 10);
    }

    #[test]
    fn test_slurm_script_directives_parsing_missing_key() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile=AMD Epyc 7742
#SBATCH --nodes=3
#SBATCH --tasks-per-node=5
#SBATCH --cpus-per-task=10
echo "Hello, World!"
"#;

        let result = SlurmScriptDirectives::from_file_contents(script_contents);

        assert!(matches!(
            result,
            Err(SlurmScriptDirectivesParsingError::MissingKey(_))
        ));
    }

    #[test]
    fn test_slurm_script_directives_parsing_invalid_value() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile=AMD Epyc 7742
#SBATCH --time=01:30:00
#SBATCH --nodes=invalid_nodes
#SBATCH --tasks-per-node=5
#SBATCH --cpus-per-task=10
echo "Hello, World!"
"#;
        let result = SlurmScriptDirectives::from_file_contents(script_contents);

        assert!(matches!(
            result,
            Err(SlurmScriptDirectivesParsingError::ParseError(_, _))
        ));
    }

    #[test]
    fn test_slurm_script_directives_parsing_invalid_date_value() {
        let script_contents = r#"#!/bin/bash
#GUILT --cpu-profile=AMD Epyc 7742
#SBATCH --time=invalid_time
#SBATCH --nodes=3
#SBATCH --tasks-per-node=5
#SBATCH --cpus-per-task=10
echo "Hello, World!"
"#;

        let result = SlurmScriptDirectives::from_file_contents(script_contents);

        assert!(matches!(
            result,
            Err(SlurmScriptDirectivesParsingError::DurationParseError(_, _))
        ));
    }
}
