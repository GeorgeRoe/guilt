use crate::slurm::node::Node;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct JobRuntimeInfo {
    pub partition: String,
    pub nodes: Vec<Node>,
}

#[derive(Serialize, Deserialize, Clone)]
pub enum CpuProfileResolutionData {
    Name(String),
    JobRuntimeInfo(JobRuntimeInfo)
}

#[derive(Serialize, Deserialize, Clone)]
pub struct UnprocessedJob {
    pub job_id: String,
    pub cpu_profile_resolution_data: CpuProfileResolutionData
}