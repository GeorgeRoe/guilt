
use crate::safe_command::{SafeCommandError, safe_get_stdout};
use std::collections::HashSet;
use std::process::Command;

pub fn get_all_partitions() -> Result<HashSet<String>, SafeCommandError> {
    let output = Command::new("sinfo")
        .arg("-s")
        .arg("-h")
        .arg("-o")
        .arg("\"%P\"")
        .output();

    Ok(safe_get_stdout(output)?.lines().map(String::from).collect())
}
