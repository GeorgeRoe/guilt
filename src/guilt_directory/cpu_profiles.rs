use crate::json_io::*;
use crate::models::CpuProfile;
use std::collections::HashMap;
use std::path::Path;

pub struct CpuProfiles {
    cache: HashMap<String, CpuProfile>,
}

impl CpuProfiles {
    pub fn empty() -> Self {
        Self {
            cache: HashMap::new(),
        }
    }

    pub fn read(path: &Path) -> Result<Self, JsonFileOperationError> {
        let profiles: Vec<CpuProfile> = read_json_file(path)?;
        let cache = profiles.into_iter().map(|p| (p.name.clone(), p)).collect();
        Ok(Self { cache })
    }

    pub fn write(&self, path: &Path) -> Result<(), JsonFileOperationError> {
        let profiles: Vec<&CpuProfile> = self.cache.values().collect();
        write_json_file(path, &profiles)
    }

    pub fn get(&self, name: &str) -> Option<CpuProfile> {
        self.cache.get(name).cloned()
    }

    pub fn upsert(&mut self, profile: CpuProfile) {
        self.cache.insert(profile.name.clone(), profile);
    }

    pub fn remove(&mut self, name: &str) {
        self.cache.remove(name);
    }
}
