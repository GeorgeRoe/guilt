use crate::guilt_directory::{migrate_current_user, MigrationStatus};

pub fn run() -> anyhow::Result<()> {
    println!("Migration!");



    match migrate_current_user()? {
        MigrationStatus::NotNeeded => {
            println!("No migration needed.");
        }
        MigrationStatus::Success => {
            println!("Migration completed successfully.");
        }
    }

    Ok(())
}