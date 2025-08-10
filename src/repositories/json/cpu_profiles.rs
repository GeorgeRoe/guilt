use crate::repositories::cpu_profiles::CpuProfilesRepository;
use crate::models::CpuProfile;
use std::path::PathBuf;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::result::Result;
use crate::SomeError;
use std::collections::HashMap;

pub struct JsonCpuProfilesRepository {
    path: PathBuf,
    profiles: HashMap<String, CpuProfile>
}

impl JsonCpuProfilesRepository {
    pub fn new(path: PathBuf) -> Result<Self, SomeError> {
        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let data: Vec<CpuProfile> = serde_json::from_reader(reader)?;

        Ok(JsonCpuProfilesRepository {
            path,
            profiles: data.into_iter().map(|profile| (profile.name.clone(), profile)).collect()
        })
    }
}

impl CpuProfilesRepository for JsonCpuProfilesRepository {
    fn get_all_profiles(&self) -> Result<Vec<CpuProfile>, SomeError> {
        Ok(self.profiles.values().cloned().collect())
    }

    fn get_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, SomeError> {
        Ok(self.profiles.get(name).cloned())
    }

    fn upsert_profile(&mut self, profile: CpuProfile) -> Result<(), SomeError> {
        self.profiles.insert(profile.name.clone(), profile);
        Ok(())
    }

    fn delete_profile(&mut self, name: &str) -> Result<(), SomeError> {
        self.profiles.remove(name);
        Ok(())
    }

    fn commit(&self) -> Result<(), SomeError> {
        let file = File::open(&self.path)?;
        let writer = BufWriter::new(file);
        let data = self.get_all_profiles()?;

        serde_json::to_writer_pretty(writer, &data)?;
        Ok(())
    }
}