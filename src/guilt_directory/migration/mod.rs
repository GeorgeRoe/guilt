use crate::users::User;
use fs_extra::dir::{copy, CopyOptions};
use std::path::Path;

mod types;
pub use types::*;

mod migrate;
use migrate::all_migrations;

pub fn migrate_user(user: &User, backup_dir: &Path) -> Result<MigrationStatus, MigrationError> {
    let mut copy_options = CopyOptions::new();
    copy_options.overwrite = true;
    copy_options.copy_inside = true;
    copy_options.content_only = true;
    let guilt_dir = user.home_dir.join(".guilt");

    let mut status = MigrationStatus::NotNeeded;
    for migration in all_migrations() {
        if migration.detect_applicable(&user) {

            copy(&guilt_dir, &backup_dir, &copy_options).map_err(|_| MigrationError::BackupError())?;

            match migration.migrate(&user) {
                Ok(_) => {
                    status = MigrationStatus::Success;
                },
                Err(e) => {
                    return Err(MigrationError::MigrationFailed(e));
                }
            }
        }
    }

    Ok(status)
}