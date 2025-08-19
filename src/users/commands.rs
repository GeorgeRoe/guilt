use super::parsing::ParseGetentPasswdError;
use super::types::User;
use crate::safe_command::{SafeCommandError, safe_get_stdout};
use std::env;
use std::process::Command;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum UserCommandError {
    #[error("Failed to execute getent passwd command: {0}")]
    SafeCommand(#[from] SafeCommandError),

    #[error("Failed to parse user data: {0}")]
    Parse(#[from] ParseGetentPasswdError),

    #[error("Environment variable not set: {0}")]
    EnvironmentVariableNotSet(String),
}

pub fn get_all_users() -> Result<Vec<User>, UserCommandError> {
    let output = Command::new("getent").arg("passwd").output();

    let stdout = safe_get_stdout(output).map_err(UserCommandError::SafeCommand)?;

    let lines = stdout.lines();

    let users = lines
        .map(User::from_getent_passwd_line)
        .collect::<Result<Vec<User>, _>>()?;

    Ok(users)
}

pub fn get_current_user() -> Result<User, UserCommandError> {
    let username = env::var("USER")
        .map_err(|_| UserCommandError::EnvironmentVariableNotSet("USER".to_string()))?;

    let output = Command::new("getent").arg("passwd").arg(&username).output();

    let stdout = safe_get_stdout(output).map_err(UserCommandError::SafeCommand)?;

    let user = User::from_getent_passwd_line(&stdout).map_err(UserCommandError::Parse)?;

    Ok(user)
}
