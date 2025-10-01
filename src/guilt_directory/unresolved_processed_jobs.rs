use std::collections::HashMap;
use std::path::Path;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use crate::models::{
    CpuProfile,
    ProcessedJob,
};
use crate::json_io::*;

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

pub struct UnresolvedProcessedJobs {
    cache: HashMap<String, UnresolvedProcessedJob>,
}

impl UnresolvedProcessedJobs {
    pub fn empty() -> Self {
        Self {
            cache: HashMap::new(),
        }
    }

    pub fn read(path: &Path) -> Result<Self, JsonFileOperationError> {
        let jobs: Vec<UnresolvedProcessedJob> = read_json_file(path)?;
        let cache = jobs.into_iter().map(|j| (j.job_id.clone(), j)).collect();
        Ok(Self{ cache })
    }

    pub fn write(&self, path: &Path) -> Result<(), JsonFileOperationError> {
        let jobs: Vec<&UnresolvedProcessedJob> = self.cache.values().collect();
        write_json_file(path, &jobs)
    }

    pub fn get(&self, job_id: &str) -> Option<UnresolvedProcessedJob> {
        if let Some(job) = self.cache.get(job_id) {
            Some(job.clone())
        } else {
            None
        }
    }

    pub fn all(&self) -> Vec<UnresolvedProcessedJob> {
        self.cache.values().cloned().collect()
    }

    pub fn upsert(&mut self, job: UnresolvedProcessedJob) {
        self.cache.insert(job.job_id.clone(), job);
    }

    pub fn remove(&mut self, job_id: &str) {
        self.cache.remove(job_id);
    }
}