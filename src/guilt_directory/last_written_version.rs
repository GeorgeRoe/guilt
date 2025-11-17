use crate::version::{Version, VersionFromStringError};
use std::fs::read_to_string;
use std::path::Path;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum LastWrittenVersionReadError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Invalid version string: {0}")]
    InvalidVersionString(#[from] VersionFromStringError),
}

pub struct LastWrittenVersion(Version);

impl LastWrittenVersion {
    pub fn new() -> Self {
        Self(Version::current())
    }

    pub fn read(path: &Path) -> Result<Self, LastWrittenVersionReadError> {
        let version_str = read_to_string(path)?.trim().to_string();
        let version = Version::parse_str(&version_str)?;
        Ok(Self(version))
    }

    pub fn write(&self, path: &Path) -> std::io::Result<()> {
        std::fs::write(path, self.0.to_string())
    }

    pub fn get(&self) -> &Version {
        &self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_last_written_version_success() {
        let temp_dir = tempfile::tempdir().unwrap();
        let version_file_path = temp_dir.path().join("last_written_version.txt");
        std::fs::write(&version_file_path, "1.2.3").unwrap();

        let last_written_version =
            LastWrittenVersion::read(&version_file_path).unwrap();

        assert_eq!(last_written_version.get().major, 1);
        assert_eq!(last_written_version.get().minor, 2);
        assert_eq!(last_written_version.get().patch, 3);
    }

    #[test]
    fn test_read_last_written_version_io_fail() {
        let temp_dir = tempfile::tempdir().unwrap();
        let version_file_path = temp_dir.path().join("non_existent_file.txt");

        let result = LastWrittenVersion::read(&version_file_path);

        assert!(matches!(result, Err(LastWrittenVersionReadError::Io(_))));
    }

    #[test]
    fn test_read_last_written_version_invalid_format() {
        let temp_dir = tempfile::tempdir().unwrap();
        let version_file_path = temp_dir.path().join("last_written_version.txt");
        std::fs::write(&version_file_path, "invalid_version").unwrap();

        let result = LastWrittenVersion::read(&version_file_path);

        assert!(matches!(
            result,
            Err(LastWrittenVersionReadError::InvalidVersionString(_))
        ));
    }

    #[test]
    fn test_write_last_written_version() {
        let temp_dir = tempfile::tempdir().unwrap();
        let version_file_path = temp_dir.path().join("last_written_version.txt");

        let last_written_version = LastWrittenVersion(Version {
            major: 2,
            minor: 5,
            patch: 1,
        });

        last_written_version
            .write(&version_file_path)
            .unwrap();

        let written_content =
            std::fs::read_to_string(&version_file_path).unwrap();
        assert_eq!(written_content, "2.5.1");
    }

    #[test]
    fn test() {
        let version = Version {
            major: 1,
            minor: 2,
            patch: 3,
        };

        let last_written_version = LastWrittenVersion(version);

        assert_eq!(last_written_version.get().major, 1);
        assert_eq!(last_written_version.get().minor, 2);
        assert_eq!(last_written_version.get().patch, 3);
    }
}