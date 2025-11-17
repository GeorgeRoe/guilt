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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_cpu_profiles() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("cpu_profiles.json");

        let profiles = vec![
            CpuProfile {
                name: "test_profile".to_string(),
                cores: 6,
                tdp: 60.0
            },
        ];

        write_json_file(&file_path, &profiles).unwrap();

        let cpu_profiles = CpuProfiles::read(&file_path).unwrap();

        assert_eq!(cpu_profiles.get("test_profile").unwrap().cores, 6);
        assert_eq!(cpu_profiles.get("test_profile").unwrap().tdp, 60.0);
    }
    
    #[test]
    fn test_write_cpu_profiles() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("cpu_profiles.json");

        let mut cpu_profiles = CpuProfiles::empty();
        cpu_profiles.upsert(CpuProfile {
            name: "test_profile".to_string(),
            cores: 8,
            tdp: 95.0
        });

        cpu_profiles.write(&file_path).unwrap();

        let read_profiles = CpuProfiles::read(&file_path).unwrap();
        assert_eq!(read_profiles.get("test_profile").unwrap().cores, 8);
        assert_eq!(read_profiles.get("test_profile").unwrap().tdp, 95.0);
    }

    #[test]
    fn test_upsert_and_remove_cpu_profiles() {
        let mut cpu_profiles = CpuProfiles::empty();

        cpu_profiles.upsert(CpuProfile {
            name: "test_profile".to_string(),
            cores: 4,
            tdp: 40.0
        });

        assert_eq!(cpu_profiles.get("test_profile").unwrap().cores, 4);
        assert_eq!(cpu_profiles.get("test_profile").unwrap().tdp, 40.0);

        cpu_profiles.remove("test_profile");
        
        assert!(cpu_profiles.get("test_profile").is_none());
    }
}