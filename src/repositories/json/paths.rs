use std::path::PathBuf;

pub const USER_DATA_DIR: &str = "user_data";

pub const CPU_PROFILES_FILE: &str = "cpu_profiles.json";
pub const UNPROCESSED_JOBS_FILE: &str = "unprocessed_jobs.json";
pub const PROCESSED_JOBS_FILE: &str = "processed_jobs.json";

pub fn user_data_dir_given_guilt_dir(guilt_dir: &PathBuf) -> PathBuf {
    guilt_dir.join(USER_DATA_DIR)
}

pub fn cpu_profiles_file_given_guilt_dir(guilt_dir: &PathBuf) -> PathBuf {
    user_data_dir_given_guilt_dir(guilt_dir).join(CPU_PROFILES_FILE)
}

pub fn unprocessed_jobs_file_given_guilt_dir(guilt_dir: &PathBuf) -> PathBuf {
    user_data_dir_given_guilt_dir(guilt_dir).join(UNPROCESSED_JOBS_FILE)
}

pub fn processed_jobs_file_given_guilt_dir(guilt_dir: &PathBuf) -> PathBuf {
    user_data_dir_given_guilt_dir(guilt_dir).join(PROCESSED_JOBS_FILE)
}
