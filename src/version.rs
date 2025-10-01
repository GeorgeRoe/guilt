use thiserror::Error;
use std::cmp::Ordering;

pub struct Version {
    pub major: u32,
    pub minor: u32,
    pub patch: u32,
}

#[derive(Error, Debug)]
pub enum VersionFromStringError {
    #[error("Invalid version format")]
    InvalidFormat,

    #[error("Failed to parse integer from version string")]
    ParseIntError(#[from] std::num::ParseIntError),
}

impl Version {
    pub fn current() -> Self {
        Self::from_str(env!("CARGO_PKG_VERSION")).expect("Current version is invalid") // should never fail
    }

    pub fn new(major: u32, minor: u32, patch: u32) -> Self {
        Self { major, minor, patch }
    }

    pub fn from_str(version_str: &str) -> Result<Self, VersionFromStringError> {
        let parts: Vec<&str> = version_str.split('.').collect();
        match parts.len() {
            3 => {
                let major = parts[0].parse()?;
                let minor = parts[1].parse()?;
                let patch = parts[2].parse()?;
                Ok(Self { major, minor, patch })
            },
            _ => Err(VersionFromStringError::InvalidFormat),
        }
    }

    fn cmp(&self, other: &Self) -> Ordering {
        match self.major.cmp(&other.major) {
            Ordering::Equal => match self.minor.cmp(&other.minor) {
                Ordering::Equal => self.patch.cmp(&other.patch),
                ord => ord,
            },
            ord => ord,
        }
    }
}

impl std::fmt::Display for Version {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)
    }
}

impl PartialEq for Version {
    fn eq(&self, other: &Self) -> bool {
        self.major == other.major && self.minor == other.minor && self.patch == other.patch
    }
}

impl Eq for Version {}

impl PartialOrd for Version {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Version {
    fn cmp(&self, other: &Self) -> Ordering {
        self.cmp(other)
    }
}