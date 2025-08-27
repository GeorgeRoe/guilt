use super::HpcPreset;
use crate::models::CpuProfile;
use crate::safe_command::safe_get_stdout;
use std::process::Command;

pub struct Isambard3GracePreset;

impl HpcPreset for Isambard3GracePreset {
    fn get_name(&self) -> &str {
        "Isambard 3 Grace"
    }

    fn is_current(&self) -> bool {
        let output = Command::new("hostname").arg("-f").output();

        let stdout = safe_get_stdout(output);

        match stdout {
            Ok(hostname) => hostname.contains("isambard"), // TODO: filter between different isambard3 systems
            Err(_) => false,
        }
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::nvidia_grace_cpu_superchip_processor()].to_vec()
    }
}
