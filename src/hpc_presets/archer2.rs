use super::HpcPreset;
use crate::models::CpuProfile;

pub struct Archer2Preset;

impl HpcPreset for Archer2Preset {
    fn get_name(&self) -> &str {
        "ARCHER2"
    }

    fn is_current(&self) -> bool {
        false
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::amd_epyc_7742()].to_vec()
    }
}
