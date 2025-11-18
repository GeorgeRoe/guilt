use crate::json_io::*;
use crate::models::{CpuProfile, ProcessedJob};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

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
    pub fn resolve(&self, cpu_profile: &CpuProfile) -> ProcessedJob {
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

    pub fn unresolve(job: &ProcessedJob) -> Self {
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
        Ok(Self { cache })
    }

    pub fn write(&self, path: &Path) -> Result<(), JsonFileOperationError> {
        let jobs: Vec<&UnresolvedProcessedJob> = self.cache.values().collect();
        write_json_file(path, &jobs)
    }

    pub fn get(&self, job_id: &str) -> Option<UnresolvedProcessedJob> {
        self.cache.get(job_id).cloned()
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unresolved_processed_job_resolve_unresolve() {
        let cpu_profile = CpuProfile {
            name: "TestProfile".to_string(),
            cores: 6,
            tdp: 60.0,
        };

        let processed_job = ProcessedJob {
            start_time: Utc::now(),
            end_time: Utc::now(),
            job_id: "1".to_string(),
            cpu_profile: cpu_profile.clone(),
            energy: 100.0,
            emissions: 50.0,
            generation_mix: HashMap::new(),
        };

        let unresolved_job = UnresolvedProcessedJob::unresolve(&processed_job);

        assert_eq!(unresolved_job.start_time, processed_job.start_time);
        assert_eq!(unresolved_job.end_time, processed_job.end_time);
        assert_eq!(unresolved_job.job_id, processed_job.job_id);
        assert_eq!(unresolved_job.cpu_profile_name, cpu_profile.name);
        assert_eq!(unresolved_job.energy, processed_job.energy);
        assert_eq!(unresolved_job.emissions, processed_job.emissions);
        assert_eq!(unresolved_job.generation_mix, processed_job.generation_mix);

        let resolved_job = unresolved_job.resolve(&cpu_profile);

        assert_eq!(resolved_job.start_time, processed_job.start_time);
        assert_eq!(resolved_job.end_time, processed_job.end_time);
        assert_eq!(resolved_job.job_id, processed_job.job_id);
        assert_eq!(resolved_job.cpu_profile.name, processed_job.cpu_profile.name);
        assert_eq!(resolved_job.energy, processed_job.energy);
        assert_eq!(resolved_job.emissions, processed_job.emissions);
        assert_eq!(resolved_job.generation_mix, processed_job.generation_mix);
    }

    fn test_read_unresolved_processed_jobs() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("processed_jobs.json");

        let time = Utc::now();

        let processed_jobs = vec![
            UnresolvedProcessedJob {
                start_time: time,
                end_time: time,
                job_id: "1".to_string(),
                cpu_profile_name: "TestProfile".to_string(),
                energy: 100.0,
                emissions: 50.0,
                generation_mix: HashMap::new(),
            }
        ];

        write_json_file(&file_path, &processed_jobs).unwrap();

        let unresolved_processed_jobs = UnresolvedProcessedJobs::read(&file_path).unwrap();

        if let Some(unresolved_job) = unresolved_processed_jobs.get("1") {
            assert_eq!(processed_job.start_time, time);
            assert_eq!(processed_job.end_time, time);
            assert_eq!(processed_job.cpu_profile_name, "TestProfile");
            assert_eq!(processed_job.energy, 100.0);
            assert_eq!(processed_job.emissions, 50.0);
            assert_eq!(processed_job.generation_mix.len(), 0);
        } else {
            panic!("Processed job not found");
        }
    }

    fn test_write_unresolved_processed_jobs() {
        let temp_dir = tempfile::tempdir().unwrap();
        let file_path = temp_dir.path().join("processed_jobs.json");

        let time = Utc::now();

        let mut unresolved_processed_jobs = UnresolvedProcessedJobs::empty();
        unresolved_processed_jobs.upsert(UnresolvedProcessedJob {
            start_time: time,
            end_time: time,
            job_id: "1".to_string(),
            cpu_profile_name: "TestProfile".to_string(),
            energy: 100.0,
            emissions: 50.0,
            generation_mix: HashMap::new(),
        });

        unresolved_processed_jobs.write(&file_path).unwrap();

        let read_jobs = UnresolvedProcessedJobs::read(&file_path).unwrap();
        if let Some(unresolved_job) = read_jobs.get("1") {
            assert_eq!(unresolved_job.start_time, time);
            assert_eq!(unresolved_job.end_time, time);
            assert_eq!(unresolved_job.cpu_profile_name, "TestProfile");
            assert_eq!(unresolved_job.energy, 100.0);
            assert_eq!(unresolved_job.emissions, 50.0);
            assert_eq!(unresolved_job.generation_mix.len(), 0);
        } else {
            panic!("Processed job not found");
        }
    }

    fn test_upsert_and_remove_unresolved_processed_jobs() {
        let mut unresolved_processed_jobs = UnresolvedProcessedJobs::empty();

        let time = Utc::now();
        unresolved_processed_jobs.upsert(UnresolvedProcessedJob {
            start_time: time,
            end_time: time,
            job_id: "1".to_string(),
            cpu_profile_name: "TestProfile".to_string(),
            energy: 100.0,
            emissions: 50.0,
            generation_mix: HashMap::new(),
        });

        if let Some(unresolved_job) = unresolved_processed_jobs.get("1") {
            assert_eq!(unresolved_job.start_time, time);
            assert_eq!(unresolved_job.end_time, time);
            assert_eq!(unresolved_job.cpu_profile_name, "TestProfile");
            assert_eq!(unresolved_job.energy, 100.0);
            assert_eq!(unresolved_job.emissions, 50.0);
            assert_eq!(unresolved_job.generation_mix.len(), 0);
        } else {
            panic!("Processed job not found");
        }

        unresolved_processed_jobs.remove("1");

        assert!(unresolved_processed_jobs.get("1").is_none());
    }
}