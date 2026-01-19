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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unresolved_unprocessed_job_resolve_unresolve() {
        let cpu_profile = CpuProfile {
            name: "test_profile".to_string(),
            cores: 4,
            tdp: 45.0,
        };

        let unprocessed_job = UnprocessedJob {
            job_id: "1".to_string(),
            cpu_profile: cpu_profile.clone(),
        };

        let unresolved_job = UnresolvedUnprocessedJob::unresolve(&unprocessed_job);

        assert_eq!(unresolved_job.job_id, "1");
        assert_eq!(unresolved_job.cpu_profile_name, "test_profile");

        let resolved_job = unresolved_job.resolve(&cpu_profile);

        assert_eq!(resolved_job.job_id, "1");
        assert_eq!(resolved_job.cpu_profile.name, "test_profile");
        assert_eq!(resolved_job.cpu_profile.cores, 4);
        assert_eq!(resolved_job.cpu_profile.tdp, 45.0);
    }

    #[test]
    fn test_read_unresolved_unprocessed_jobs() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("unprocessed_jobs.json");

        let unprocessed_jobs = vec![UnresolvedUnprocessedJob {
            job_id: "1".to_string(),
            cpu_profile_name: "TestProfile".to_string(),
        }];

        write_json_file(&file_path, &unprocessed_jobs).unwrap();

        let unresolved_unprocessed_jobs = UnresolvedUnprocessedJobs::read(&file_path).unwrap();

        let unresolved_unprocessed_job = unresolved_unprocessed_jobs.get("1").unwrap();

        assert_eq!(unresolved_unprocessed_job.cpu_profile_name, "TestProfile");
    }

    #[test]
    fn test_write_unresolved_unprocessed_jobs() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("unprocessed_jobs.json");

        let mut unresolved_unprocessed_jobs = UnresolvedUnprocessedJobs::empty();
        unresolved_unprocessed_jobs.upsert(UnresolvedUnprocessedJob {
            job_id: "1".to_string(),
            cpu_profile_name: "TestProfile".to_string(),
        });

        unresolved_unprocessed_jobs.write(&file_path).unwrap();

        let read_jobs = UnresolvedUnprocessedJobs::read(&file_path).unwrap();

        let unresolved_unprocessed_job = read_jobs.get("1").unwrap();

        assert_eq!(unresolved_unprocessed_job.cpu_profile_name, "TestProfile");
    }

    #[test]
    fn test_upsert_and_remove_unresolved_unprocessed_jobs() {
        let mut unresolved_unprocessed_jobs = UnresolvedUnprocessedJobs::empty();

        unresolved_unprocessed_jobs.upsert(UnresolvedUnprocessedJob {
            job_id: "1".to_string(),
            cpu_profile_name: "TestProfile".to_string(),
        });

        let unresolved_unprocessed_job = unresolved_unprocessed_jobs.get("1").unwrap();

        assert_eq!(unresolved_unprocessed_job.cpu_profile_name, "TestProfile");

        unresolved_unprocessed_jobs.remove("1");

        assert!(unresolved_unprocessed_jobs.get("1").is_none());
    }
}
