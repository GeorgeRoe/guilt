use super::Migration;
use crate::users::User;
use std::fs;

pub struct MigrateToRepoMigrations;

impl Migration for MigrateToRepoMigrations {
    fn migrate(&self, user: &User) -> anyhow::Result<()> {
        let guilt_dir = user.home_dir.join(".guilt");
        let user_data_dir = guilt_dir.join("user_data");

        fs::rename(user_data_dir.join("cpu_profiles.json"), guilt_dir.join("cpu_profiles.json"))?;
        fs::rename(user_data_dir.join("processed_jobs.json"), guilt_dir.join("processed_jobs.json"))?;
        fs::rename(user_data_dir.join("unprocessed_jobs.json"), guilt_dir.join("unprocessed_jobs.json"))?;
        fs::remove_dir_all(user_data_dir)?;

        Ok(())
    }

    fn detect_applicable(&self, user: &User) -> bool {
        user.home_dir.join(".guilt/user_data").exists()
    }
}