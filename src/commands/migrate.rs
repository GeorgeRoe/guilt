use crate::guilt_directory::{MigrationStatus, migrate_current_user};
use crate::users::get_current_user;

pub fn run() -> anyhow::Result<()> {
    let backup_dir = get_current_user()?.home_dir.join(".guilt.bak");

    match migrate_current_user(&backup_dir)? {
        MigrationStatus::NotNeeded => {
            println!("No migration needed.");
        }
        MigrationStatus::Success => {
            println!("Migration completed successfully.");
            println!(
                "Your old data has been backed up to: {}",
                backup_dir.display()
            );
        }
    }

    Ok(())
}
