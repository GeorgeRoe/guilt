use crate::models::CpuProfile;
use std::result::Result;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CpuProfilesRepositoryError {}

pub trait CpuProfilesRepository {
    fn get_all_cpu_profiles(&self) -> Result<Vec<CpuProfile>, CpuProfilesRepositoryError>;
    fn get_cpu_profile_by_name(&self, name: &str) -> Result<Option<CpuProfile>, CpuProfilesRepositoryError>;
    fn upsert_cpu_profile(&mut self, profile: &CpuProfile) -> Result<(), CpuProfilesRepositoryError>;
    fn delete_cpu_profile(&mut self, name: &str) -> Result<(), CpuProfilesRepositoryError>;
}
