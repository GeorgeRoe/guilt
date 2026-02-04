use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone)]
pub enum CpuProfileResolutionData {
    Name(String),
    None
}

#[derive(Serialize, Deserialize, Clone)]
pub struct UnprocessedJob {
    pub job_id: String,
    pub cpu_profile_resolution_data: CpuProfileResolutionData
}