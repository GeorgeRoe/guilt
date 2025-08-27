use super::HpcPreset;
use crate::models::CpuProfile;

pub struct Isambard3GracePreset;

impl HpcPreset for Isambard3GracePreset {
    fn get_name(&self) -> &str {
        "Isambard 3 Grace"
    }

    fn is_current(&self) -> bool {
        false
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::nvidia_grace_cpu_superchip_processor()].to_vec()
    }
}
