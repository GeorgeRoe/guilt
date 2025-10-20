use std::path::PathBuf;
use tempfile::{TempDir, tempdir};

pub struct User {
    pub name: String,
    pub gecos: String,
    pub home_dir: PathBuf,
}

pub struct TestingUser {
    pub user: User,
    _tempdir: TempDir,
}

impl TestingUser {
    pub fn new(name: &str, gecos: &str) -> anyhow::Result<Self> {
        let temp_dir = tempdir()?;

        let user = User {
            name: name.to_string(),
            gecos: gecos.to_string(),
            home_dir: temp_dir.path().to_path_buf(),
        };

        Ok(TestingUser {
            user,
            _tempdir: temp_dir,
        })
    }

    pub fn test_user() -> anyhow::Result<Self> {
        Self::new("testuser", "Test User")
    }
}
