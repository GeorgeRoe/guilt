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
}
