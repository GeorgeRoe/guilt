use super::JsonUserDataRepository;
use crate::SomeError;
use crate::models::CpuProfile;
use crate::repositories::CpuProfilesRepository;

impl CpuProfilesRepository for JsonUserDataRepository {
    fn get_all_cpu_profiles(&self) -> Result<Vec<CpuProfile>, SomeError> {
        Ok(self.cpu_profiles.values().cloned().collect())
    }

    fn get_cpu_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, SomeError> {
        Ok(self.cpu_profiles.get(name).cloned())
    }

    fn upsert_cpu_profile(&mut self, profile: &CpuProfile) -> Result<(), SomeError> {
        self.cpu_profiles
            .insert(profile.name.clone(), profile.clone());
        Ok(())
    }

    fn delete_cpu_profile(&mut self, name: &str) -> Result<(), SomeError> {
        self.cpu_profiles.remove(name);
        Ok(())
    }
}
