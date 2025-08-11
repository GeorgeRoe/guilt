use crate::models::CpuProfile;
use std::result::Result;
use crate::SomeError;

pub trait CpuProfilesRepository {
    fn get_all_cpu_profiles(&self) -> Result<Vec<CpuProfile>, SomeError>;
    fn get_cpu_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, SomeError>;
    fn upsert_cpu_profile(&mut self, profile: &CpuProfile) -> Result<(), SomeError>;
    fn delete_cpu_profile(&mut self, name: &str) -> Result<(), SomeError>;
}
