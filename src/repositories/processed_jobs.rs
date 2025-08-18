use crate::models::ProcessedJob;
use std::result::Result;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ProcessedJobsRepositoryError {
    #[error("Referenced CPU profile not found: {0}")]
    MissingCpuProfile(String)
}

pub trait ProcessedJobsRepository {
    fn get_all_processed_jobs(&self) -> Result<Vec<ProcessedJob>, ProcessedJobsRepositoryError>;
    fn get_processed_job_by_id(&self, id: &str) -> Result<Option<ProcessedJob>, ProcessedJobsRepositoryError>;
    fn upsert_processed_job(&mut self, job: &ProcessedJob) -> Result<(), ProcessedJobsRepositoryError>;
    fn delete_processed_job(&mut self, id: &str) -> Result<(), ProcessedJobsRepositoryError>;
}
