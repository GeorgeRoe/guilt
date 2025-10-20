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
