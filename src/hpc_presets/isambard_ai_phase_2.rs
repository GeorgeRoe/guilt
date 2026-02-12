use super::HpcPreset;
use crate::models::CpuProfile;

pub struct IsambardAiPhase2Preset;

impl HpcPreset for IsambardAiPhase2Preset {
    fn get_name(&self) -> &str {
        "Isambard-AI Phase 2"
    }

    fn is_current(&self) -> bool {
        false
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::nvidia_gh200_grace_hopper_superchip_processor()].to_vec()
    }

    fn get_profile_resolution_policy_script(&self) -> Option<String> {
        None
    }
}
