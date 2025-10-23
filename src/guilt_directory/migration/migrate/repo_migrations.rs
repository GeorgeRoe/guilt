use super::Migration;
use crate::users::User;
use std::fs;

pub struct MigrateToRepoMigrations;

impl Migration for MigrateToRepoMigrations {
    fn migrate(&self, user: &User) -> anyhow::Result<()> {
        let guilt_dir = user.home_dir.join(".guilt");
        let user_data_dir = guilt_dir.join("user_data");

        fs::rename(
            user_data_dir.join("cpu_profiles.json"),
            guilt_dir.join("cpu_profiles.json"),
        )?;
        fs::rename(
            user_data_dir.join("processed_jobs.json"),
            guilt_dir.join("processed_jobs.json"),
        )?;
        fs::rename(
            user_data_dir.join("unprocessed_jobs.json"),
            guilt_dir.join("unprocessed_jobs.json"),
        )?;
        fs::write(
            guilt_dir.join("last_written_version"),
            b"1.1.1",
        )?;
        fs::remove_dir_all(user_data_dir)?;

        Ok(())
    }

    fn detect_applicable(&self, user: &User) -> bool {
        user.home_dir.join(".guilt/user_data").exists()
    }
}

#[cfg(test)]
mod tests {
    use super::{MigrateToRepoMigrations, Migration};
    use crate::users::TestingUser;
    use std::fs;

    fn setup_testing_user_with_previous_structure() -> anyhow::Result<TestingUser> {
        let testing_user = TestingUser::test_user()?;

        let guilt_dir = testing_user.user.home_dir.join(".guilt");

        let user_data_dir = guilt_dir.join("user_data");

        fs::create_dir_all(&user_data_dir)?;
        fs::write(user_data_dir.join("cpu_profiles.json"), b"{}")?;
        fs::write(user_data_dir.join("processed_jobs.json"), b"{}")?;
        fs::write(user_data_dir.join("unprocessed_jobs.json"), b"{}")?;

        Ok(testing_user)
    }

    #[test]
    fn detect_applicable_when_user_data_exists() -> anyhow::Result<()> {
        let testing_user = setup_testing_user_with_previous_structure()?;

        let migration = MigrateToRepoMigrations;

        assert!(migration.detect_applicable(&testing_user.user));

        Ok(())
    }

    #[test]
    fn migrate_moves_files_and_removes_user_data_dir() -> anyhow::Result<()> {
        let testing_user = setup_testing_user_with_previous_structure()?;

        let migration = MigrateToRepoMigrations;

        migration.migrate(&testing_user.user)?;

        let guilt_dir = testing_user.user.home_dir.join(".guilt");

        assert!(guilt_dir.join("cpu_profiles.json").exists());
        assert!(guilt_dir.join("processed_jobs.json").exists());
        assert!(guilt_dir.join("unprocessed_jobs.json").exists());
        assert!(guilt_dir.join("last_written_version").exists());
        assert!(!guilt_dir.join("user_data").exists());

        Ok(())
    }
}
