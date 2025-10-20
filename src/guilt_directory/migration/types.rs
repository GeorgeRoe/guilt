use crate::users::User;
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
    BackupError()
}

pub enum MigrationStatus {
    NotNeeded,
    Success
}