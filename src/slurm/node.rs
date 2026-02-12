use crate::safe_command::{SafeCommandError, safe_get_stdout};
use rhai::{CustomType, TypeBuilder};
use serde::{Deserialize, Serialize};
use std::process::Command;
use thiserror::Error;

#[derive(Debug, Deserialize, Serialize, Clone, CustomType)]
pub struct Node {
    pub architecture: String,

    pub cores: i32,

    pub cpus: i32,

    pub features: Vec<String>,

    pub name: String,

    pub operating_system: String,

    pub partitions: Vec<String>,

    #[serde(rename(deserialize = "real_memory", serialize = "memory"))]
    pub memory: u64,

    pub sockets: i32,

    pub threads: i32,
}

#[derive(Deserialize)]
pub struct ScontrolShowNodeResponse {
    nodes: Vec<Node>
}

#[derive(Debug, Error)]
pub enum SlurmControlShowNodeCommandError {
    #[error("Failed to execute Slurm control command: {0}")]
    SafeCommand(#[from] SafeCommandError),

    #[error("Failed to parse Slurm control JSON output: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Node '{0}' not found.")]
    NodeNotFound(String),
}

pub fn get_node_by_name(name: &str) -> Result<Node, SlurmControlShowNodeCommandError> {
    let output = Command::new("scontrol")
        .arg("show")
        .arg("node")
        .arg(name)
        .arg("--json")
        .output();

    let stdout = safe_get_stdout(output)?;

    let response: ScontrolShowNodeResponse = serde_json::from_str(&stdout)?;

    match response.nodes.first() {
        Some(node) => Ok(node.clone()),
        None => Err(SlurmControlShowNodeCommandError::NodeNotFound(
            name.to_string(),
        )),
    }
}
