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
        if let Some(cpu_profile) = self.cache.get(name) {
            Some(cpu_profile.clone())
        } else {
            None
        }
    }

    pub fn upsert(&mut self, profile: CpuProfile) {
        self.cache.insert(profile.name.clone(), profile);
    }

    pub fn remove(&mut self, name: &str) {
        self.cache.remove(name);
    }
}
