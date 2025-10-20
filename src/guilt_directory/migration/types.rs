use crate::users::{User, UserCommandError};
use thiserror::Error;

pub trait Migration {
    fn migrate(&self, user: &User) -> anyhow::Result<()>;
    fn detect_applicable(&self, user: &User) -> bool;
}

#[derive(Error, Debug)]
pub enum MigrationError {
    #[error("Migration failed: {0}")]
    MigrationFailed(#[from] anyhow::Error),

    #[error("Failed to backup .guilt directory")]
    BackupError(),
}

#[derive(Error, Debug)]
pub enum CurrentUserMigrationError {
    #[error("Failed to get current user: {0}")]
    UserError(#[from] UserCommandError),

    #[error("Migration failed: {0}")]
    MigrationError(#[from] MigrationError),
}

pub enum MigrationStatus {
    NotNeeded,
    Success,
}
