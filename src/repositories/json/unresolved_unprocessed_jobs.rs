use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::result::Result;
use crate::SomeError;
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedUnprocessedJob {
    pub job_id: String,
    pub cpu_profile_name: String
}

pub struct JsonUnresolvedUnprocessedJobsRepository {
    path: PathBuf,
    jobs: HashMap<String, UnresolvedUnprocessedJob>
}

impl JsonUnresolvedUnprocessedJobsRepository {
    pub fn new(path: PathBuf) -> Result<Self, SomeError> {
        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let data: Vec<UnresolvedUnprocessedJob> = serde_json::from_reader(reader)?;

        Ok(JsonUnresolvedUnprocessedJobsRepository {
            path,
            jobs: data.into_iter().map(|job| (job.job_id.clone(), job)).collect()
        })
    }

    pub fn get_all_jobs(&self) -> Vec<UnresolvedUnprocessedJob> {
        self.jobs.values().cloned().collect()
    }

    pub fn get_job_by_id(&self, job_id: &str) -> Option<UnresolvedUnprocessedJob> {
        self.jobs.get(job_id).cloned()
    }

    pub fn upsert_job(&mut self, job: &UnresolvedUnprocessedJob) {
        self.jobs.insert(job.job_id.clone(), job.clone());
    }

    pub fn delete_job(&mut self, job_id: &str) {
        self.jobs.remove(job_id);
    }

    pub fn commit(&self) -> Result<(), SomeError> {
        let file = File::open(&self.path)?;
        let writer = BufWriter::new(file);
        let data = self.get_all_jobs();

        serde_json::to_writer_pretty(writer, &data)?;
        Ok(())
    }
}