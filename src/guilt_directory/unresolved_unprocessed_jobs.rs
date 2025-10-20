use crate::json_io::*;
use crate::models::{CpuProfile, UnprocessedJob};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

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

pub struct UnresolvedUnprocessedJobs {
    cache: HashMap<String, UnresolvedUnprocessedJob>,
}

impl UnresolvedUnprocessedJobs {
    pub fn empty() -> Self {
        Self {
            cache: HashMap::new(),
        }
    }

    pub fn read(path: &Path) -> Result<Self, JsonFileOperationError> {
        let jobs: Vec<UnresolvedUnprocessedJob> = read_json_file(path)?;
        let cache = jobs.into_iter().map(|j| (j.job_id.clone(), j)).collect();
        Ok(Self { cache })
    }

    pub fn write(&self, path: &Path) -> Result<(), JsonFileOperationError> {
        let jobs: Vec<&UnresolvedUnprocessedJob> = self.cache.values().collect();
        write_json_file(path, &jobs)
    }

    pub fn get(&self, job_id: &str) -> Option<UnresolvedUnprocessedJob> {
        self.cache.get(job_id).cloned()
    }

    pub fn all(&self) -> Vec<UnresolvedUnprocessedJob> {
        self.cache.values().cloned().collect()
    }

    pub fn upsert(&mut self, job: UnresolvedUnprocessedJob) {
        self.cache.insert(job.job_id.clone(), job);
    }

    pub fn remove(&mut self, job_id: &str) {
        self.cache.remove(job_id);
    }
}
