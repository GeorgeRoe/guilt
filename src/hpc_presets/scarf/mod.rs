use super::HpcPreset;
use crate::models::CpuProfile;
use crate::safe_command::safe_get_stdout;
use std::process::Command;

pub struct ScarfPreset;

impl HpcPreset for ScarfPreset {
    fn get_name(&self) -> &str {
        "SCARF"
    }

    fn is_current(&self) -> bool {
        let output = Command::new("hostname").arg("-f").output();

        let stdout = safe_get_stdout(output);

        match stdout {
            Ok(hostname) => hostname.contains("scarf"),
            Err(_) => false,
        }
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [
            CpuProfile::amd_epyc_7302(),
            CpuProfile::amd_epyc_7502(),
            CpuProfile::amd_epyc_9654(),
        ]
        .to_vec()
    }

    fn get_profile_resolution_policy_script(&self) -> Option<String> {
        Some(include_str!("profile_resolution_policy.rhai").to_string())
    }
}
