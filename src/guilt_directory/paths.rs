use crate::users::User;
use std::path::PathBuf;

pub const CPU_PROFILES_FILE: &str = "cpu_profiles.json";
pub const UNPROCESSED_JOBS_FILE: &str = "unprocessed_jobs.json";
pub const PROCESSED_JOBS_FILE: &str = "processed_jobs.json";
pub const LAST_WRITTEN_VERSION_FILE: &str = "last_written_version";
pub const PROFILE_RESOLUTION_POLICY_FILE: &str = "profile_resolution_policy.rhai";

pub const GUILT_DIR: &str = ".guilt";

pub fn guilt_directory_for_user(user: &User) -> PathBuf {
    let home_dir = user.home_dir.as_path();
    home_dir.join(GUILT_DIR)
}
