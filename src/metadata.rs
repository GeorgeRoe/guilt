use crate::users::User;
use crate::guilt_dir::guilt_dir_given_home;
use crate::json_io::{read_json_file, write_json_file, JsonFileOperationError};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};

pub const METADATA_FILE: &str = "metadata.json";

pub fn metadata_file_given_guilt_dir(guilt_dir: &Path) -> PathBuf {
    guilt_dir.join(METADATA_FILE)
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Metadata {
    pub last_commit_version: String,
}

impl Metadata {
    pub fn new(user: &User) -> Result<Self, JsonFileOperationError> {
        let guilt_dir = guilt_dir_given_home(&user.home_dir);

        let metadata_path = metadata_file_given_guilt_dir(&guilt_dir);

        read_json_file(metadata_path)
    }

    pub fn commit(&self, user: &User) -> Result<(), JsonFileOperationError> {
        let guilt_dir = guilt_dir_given_home(&user.home_dir);

        let metadata_path = metadata_file_given_guilt_dir(&guilt_dir);

        write_json_file(metadata_path, self)
    }

    pub fn current_version_matches_last_commit(&self) -> bool {
        env!("CARGO_PKG_VERSION") == self.last_commit_version
    }
}