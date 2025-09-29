use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::models::{
    CpuProfile,
    ProcessedJob,
};

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedProcessedJob {
    pub start_time: DateTime<Utc>,
    pub end_time: DateTime<Utc>,
    pub job_id: String,
    pub cpu_profile_name: String,
    pub energy: f64,
    pub emissions: f64,
    pub generation_mix: HashMap<String, f64>,
}

impl UnresolvedProcessedJob {
    pub fn resolve(
        &self,
        cpu_profile: &CpuProfile,
    ) -> ProcessedJob {
        ProcessedJob {
            start_time: self.start_time,
            end_time: self.end_time,
            job_id: self.job_id.clone(),
            cpu_profile: cpu_profile.clone(),
            energy: self.energy,
            emissions: self.emissions,
            generation_mix: self.generation_mix.clone(),
        }
    }

    pub fn unresolve(
        job: &ProcessedJob,
    ) -> Self {
        Self {
            start_time: job.start_time,
            end_time: job.end_time,
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
            energy: job.energy,
            emissions: job.emissions,
            generation_mix: job.generation_mix.clone(),
        }
    }
}