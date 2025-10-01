use std::path::Path;

pub struct LastWrittenVersion(String);

impl LastWrittenVersion {
    pub fn new() -> Self {
        Self(env!("CARGO_PKG_VERSION").to_string())
    }

    pub fn read(path: &Path) -> std::io::Result<Self> {
        let version = std::fs::read_to_string(path)?.trim().to_string();
        Ok(Self(version))
    }

    pub fn write(&self, path: &Path) -> std::io::Result<()> {
        std::fs::write(path, &self.0)
    }

    pub fn get(&self) -> &str {
        &self.0
    }
}