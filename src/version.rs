use std::cmp::Ord;
use std::cmp::Ordering;
use thiserror::Error;

#[derive(Debug, Clone)]
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
        Self::parse_str(env!("CARGO_PKG_VERSION")).expect("Current version is invalid") // should never fail
    }

    pub fn new(major: u32, minor: u32, patch: u32) -> Self {
        Self {
            major,
            minor,
            patch,
        }
    }

    pub fn parse_str(version_str: &str) -> Result<Self, VersionFromStringError> {
        let parts: Vec<&str> = version_str.split('.').collect();
        match parts.len() {
            3 => {
                let major = parts[0].parse()?;
                let minor = parts[1].parse()?;
                let patch = parts[2].parse()?;
                Ok(Self {
                    major,
                    minor,
                    patch,
                })
            }
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
        Some(Ord::cmp(self, other))
    }
}

impl Ord for Version {
    fn cmp(&self, other: &Self) -> Ordering {
        self.cmp(other)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_parsing() {
        let version = Version::parse_str("1.2.3").unwrap();
        assert_eq!(version.major, 1);
        assert_eq!(version.minor, 2);
        assert_eq!(version.patch, 3);
    }

    #[test]
    fn test_invalid_version_parsing() {
        let result = Version::parse_str("1.2");
        assert!(matches!(result, Err(VersionFromStringError::InvalidFormat)));

        let result = Version::parse_str("1.a.3");
        assert!(matches!(
            result,
            Err(VersionFromStringError::ParseIntError(_))
        ));
    }

    #[test]
    fn test_version_equality() {
        let v1 = Version::new(1, 2, 3);
        let v2 = Version::new(1, 2, 3);
        let v3 = Version::new(1, 2, 4);

        assert_eq!(v1, v2);
        assert_ne!(v1, v3);
    }

    #[test]
    fn test_version_comparison() {
        let v1 = Version::new(1, 2, 3);
        let v2 = Version::new(1, 2, 4);
        let v3 = Version::new(1, 3, 0);
        let v4 = Version::new(2, 0, 0);

        assert!(v1 < v2);
        assert!(v2 < v3);
        assert!(v3 < v4);
        assert!(v4 > v1);
    }
}
