use super::JsonUserDataRepository;
use crate::models::CpuProfile;
use crate::repositories::{CpuProfilesRepository, CpuProfilesRepositoryError};

impl CpuProfilesRepository for JsonUserDataRepository {
    fn get_all_cpu_profiles(&self) -> Result<Vec<CpuProfile>, CpuProfilesRepositoryError> {
        Ok(self.cpu_profiles.values().cloned().collect())
    }

    fn get_cpu_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, CpuProfilesRepositoryError> {
        Ok(self.cpu_profiles.get(name).cloned())
    }

    fn upsert_cpu_profile(&mut self, profile: &CpuProfile) -> Result<(), CpuProfilesRepositoryError> {
        self.cpu_profiles
            .insert(profile.name.clone(), profile.clone());
        Ok(())
    }

    fn delete_cpu_profile(&mut self, name: &str) -> Result<(), CpuProfilesRepositoryError> {
        self.cpu_profiles.remove(name);
        Ok(())
    }
}
