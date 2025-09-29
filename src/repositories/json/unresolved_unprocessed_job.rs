use serde::{Deserialize, Serialize};
use crate::models::{
    CpuProfile,
    UnprocessedJob,
};

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedUnprocessedJob {
    pub job_id: String,
    pub cpu_profile_name: String,
}

impl UnresolvedUnprocessedJob {
    pub fn resolve(&self, cpu_profile: &CpuProfile) -> UnprocessedJob {
        UnprocessedJob {
            job_id: self.job_id.clone(),
            cpu_profile: cpu_profile.clone(),
        }
    }

    pub fn unresolve(job: &UnprocessedJob) -> Self {
        Self {
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
        }
    }
}