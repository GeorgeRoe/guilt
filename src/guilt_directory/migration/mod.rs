use crate::users::{User, get_current_user};
use fs_extra::dir::{CopyOptions, copy};
use std::path::Path;

mod types;
pub use types::*;

mod migrate;
use migrate::all_migrations_in_order;

fn migrate_user(user: &User, backup_dir: &Path) -> Result<MigrationStatus, MigrationError> {
    let mut copy_options = CopyOptions::new();
    copy_options.overwrite = true;
    copy_options.copy_inside = true;
    copy_options.content_only = true;
    let guilt_dir = user.home_dir.join(".guilt");

    let mut has_been_backed_up = false;

    let mut status = MigrationStatus::NotNeeded;
    for migration in all_migrations_in_order() {
        if migration.detect_applicable(user) {
            if !has_been_backed_up {
                copy(&guilt_dir, backup_dir, &copy_options)
                    .map_err(|_| MigrationError::BackupError())?;
                has_been_backed_up = true;
            }

            match migration.migrate(user) {
                Ok(_) => {
                    status = MigrationStatus::Success;
                }
                Err(e) => {
                    return Err(MigrationError::MigrationFailed(e));
                }
            }
        }
    }

    Ok(status)
}

pub fn migrate_current_user(
    backup_dir: &Path,
) -> Result<MigrationStatus, CurrentUserMigrationError> {
    Ok(migrate_user(&get_current_user()?, backup_dir)?)
}
