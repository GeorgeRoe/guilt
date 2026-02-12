use super::HpcPreset;
use crate::models::CpuProfile;
use crate::safe_command::safe_get_stdout;
use crate::slurm::partitions::get_all_partitions;
use std::collections::HashSet;
use std::process::Command;

pub struct Isambard3MacsPreset;

impl HpcPreset for Isambard3MacsPreset {
    fn get_name(&self) -> &str {
        "Isambard 3 Macs"
    }

    fn is_current(&self) -> bool {
        let expected_partitions: HashSet<_> = [
            "milan", "genoa", "berg", "spr", "sprhbm", "ampere", "hopper", "instinct",
        ]
        .into_iter()
        .map(String::from)
        .collect();

        let hostname_output = Command::new("hostname").arg("-f").output();

        let hostname_stdout = safe_get_stdout(hostname_output);

        match (hostname_stdout, get_all_partitions()) {
            (Ok(hostname), Ok(partitions)) => {
                hostname.contains("isambard") && expected_partitions.is_subset(&partitions)
            }
            _ => false,
        }
    }

    fn get_cpu_profiles(&self) -> Vec<CpuProfile> {
        [
            CpuProfile::amd_epyc_7713(),
            CpuProfile::amd_epyc_9354(),
            CpuProfile::amd_epyc_9754(),
            CpuProfile::intel_xeon_gold_6430(),
            CpuProfile::intel_xeon_max_9462(),
            CpuProfile::amd_epyc_7543p(),
        ]
        .to_vec()
    }

    fn get_profile_resolution_policy_script(&self) -> Option<String> {
        None
    }
}
