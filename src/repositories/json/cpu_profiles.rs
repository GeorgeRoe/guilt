use super::JsonUserDataRepository;
use crate::repositories::CpuProfilesRepository;
use crate::models::CpuProfile;
use crate::SomeError;

impl CpuProfilesRepository for JsonUserDataRepository {
    fn get_all_profiles(&self) -> Result<Vec<CpuProfile>, SomeError> {
        Ok(self.cpu_profiles.values().cloned().collect())
    }

    fn get_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, SomeError> {
        Ok(self.cpu_profiles.get(name).cloned())
    }

    fn upsert_profile(&mut self, profile: &CpuProfile) -> Result<(), SomeError> {
       self.cpu_profiles.insert(profile.name.clone(), profile.clone());
       Ok(())
    }

    fn delete_profile(&mut self, name: &str) -> Result<(), SomeError> {
        self.cpu_profiles.remove(name);
        Ok(())
    }
}