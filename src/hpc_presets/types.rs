use crate::models::CpuProfile;

pub trait HpcPreset {
    fn get_name(&self) -> &str;
    fn is_current(&self) -> bool;
    fn get_cpu_profiles(&self) -> Vec<CpuProfile>;
}
