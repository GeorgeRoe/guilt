use std::process::Output;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SafeCommandError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Failed to parse output as UTF-8: {0}")]
    Utf8(#[from] std::str::Utf8Error),

    #[error("Command failed: {0}")]
    CommandFailed(String),

    #[error("Command not found: {0}")]
    CommandNotFound(String),
}

pub fn safe_get_stdout(output: Result<Output, std::io::Error>) -> Result<String, SafeCommandError> {
    match output {
        Ok(output) => {
            if !output.status.success() {
                let stderr = String::from_utf8_lossy(&output.stderr);
                Err(if stderr.contains("command not found") {
                    SafeCommandError::CommandNotFound(stderr.to_string())
                } else {
                    SafeCommandError::CommandFailed(stderr.to_string())
                })
            } else {
                str::from_utf8(&output.stdout)
                    .map(|s| s.to_string())
                    .map_err(SafeCommandError::Utf8)
            }
        }
        Err(e) => Err(SafeCommandError::Io(e)),
    }
}

pub fn safe_get_stderr(output: Result<Output, std::io::Error>) -> Result<String, SafeCommandError> {
    match output {
        Ok(output) => {
            if !output.status.success() {
                let stderr = String::from_utf8_lossy(&output.stderr);
                Err(if stderr.contains("command not found") {
                    SafeCommandError::CommandNotFound(stderr.to_string())
                } else {
                    SafeCommandError::CommandFailed(stderr.to_string())
                })
            } else {
                str::from_utf8(&output.stderr)
                    .map(|s| s.to_string())
                    .map_err(SafeCommandError::Utf8)
            }
        },
        Err(e) => Err(SafeCommandError::Io(e)),
    }
}