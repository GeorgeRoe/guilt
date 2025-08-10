use crate::models::CpuProfile;
use std::result::Result;
use crate::SomeError;

pub trait CpuProfilesRepository {
    fn get_all_profiles(&self) -> Result<Vec<CpuProfile>, SomeError>;
    fn get_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, SomeError>;
    fn upsert_profile(&mut self, profile: CpuProfile) -> Result<(), SomeError>;
    fn delete_profile(&mut self, name: &str) -> Result<(), SomeError>;
    fn commit(&self) -> Result<(), SomeError>;
}
