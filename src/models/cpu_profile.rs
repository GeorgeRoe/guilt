use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Clone)]
pub struct CpuProfile {
    pub name: String,
    pub cores: u16,
    pub tdp: f32,
}

impl CpuProfile {
    pub fn amd_epyc_7302() -> Self {
        Self {
            name: "AMD Epyc 7302".to_string(),
            cores: 16,
            tdp: 155.0,
        }
    }

    pub fn amd_epyc_7502() -> Self {
        Self {
            name: "AMD Epyc 7502".to_string(),
            cores: 32,
            tdp: 180.0,
        }
    }

    pub fn amd_epyc_7543p() -> Self {
        Self {
            name: "AMD Epyc 7543P".to_string(),
            cores: 32,
            tdp: 225.0,
        }
    }

    pub fn amd_epyc_7713() -> Self {
        Self {
            name: "AMD Epyc 7713".to_string(),
            cores: 64,
            tdp: 225.0,
        }
    }

    pub fn amd_epyc_7742() -> Self {
        Self {
            name: "AMD Epyc 7742".to_string(),
            cores: 64,
            tdp: 225.0,
        }
    }

    pub fn amd_epyc_9354() -> Self {
        Self {
            name: "AMD Epyc 9354".to_string(),
            cores: 32,
            tdp: 280.0,
        }
    }

    pub fn amd_epyc_9654() -> Self {
        Self {
            name: "AMD Epyc 9654".to_string(),
            cores: 96,
            tdp: 360.0,
        }
    }

    pub fn amd_epyc_9754() -> Self {
        Self {
            name: "AMD Epyc 9754".to_string(),
            cores: 128,
            tdp: 360.0,
        }
    }

    pub fn intel_xeon_gold_6430() -> Self {
        Self {
            name: "Intel Xeon Gold 6430".to_string(),
            cores: 32,
            tdp: 270.0,
        }
    }

    pub fn intel_xeon_max_9462() -> Self {
        Self {
            name: "Intel Xeon CPU Max 9462".to_string(),
            cores: 32,
            tdp: 350.0,
        }
    }

    pub fn nvidia_grace_cpu_superchip_processor() -> Self {
        Self {
            name: "NVIDIA Grace Superchip Processor".to_string(),
            cores: 72,
            tdp: 250.0, // TDP is a slightly wrong, this includes the memory tdp too
        }
    }
}
