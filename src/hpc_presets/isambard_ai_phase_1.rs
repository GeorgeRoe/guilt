use super::HpcPreset;
use crate::models::CpuProfile;

pub struct IsambardAiPhase1Preset;

impl HpcPreset for IsambardAiPhase1Preset {
    fn get_name(&self) -> &str {
        "Isambard-AI Phase 1"
    }

    fn is_current(&self) -> bool {
        false
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::nvidia_gh200_grace_hopper_superchip_processor()].to_vec()
    }
}