use super::HpcPreset;
use crate::models::CpuProfile;
use crate::safe_command::safe_get_stdout;
use crate::slurm::partitions::get_all_partitions;
use std::process::Command;

pub struct Isambard3GracePreset;

impl HpcPreset for Isambard3GracePreset {
    fn get_name(&self) -> &str {
        "Isambard 3 Grace"
    }

    fn is_current(&self) -> bool {
        let hostname_output = Command::new("hostname").arg("-f").output();

        let hostname_stdout = safe_get_stdout(hostname_output);

        match (hostname_stdout, get_all_partitions()) {
            (Ok(hostname), Ok(partitions)) => {
                hostname.contains("isambard") && partitions.contains("grace")
            }
            _ => false,
        }
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [CpuProfile::nvidia_grace_cpu_superchip_processor()].to_vec()
    }
}
