use crate::models::UnprocessedJob;
use std::result::Result;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UnprocessedJobsRepositoryError {
    #[error("Referenced CPU profile not found: {0}")]
    MissingCpuProfile(String)
}

pub trait UnprocessedJobsRepository {
    fn get_all_unprocessed_jobs(&self) -> Result<Vec<UnprocessedJob>, UnprocessedJobsRepositoryError>;
    fn get_unprocessed_job_by_id(&self, id: &str) -> Result<Option<UnprocessedJob>, UnprocessedJobsRepositoryError>;
    fn upsert_unprocessed_job(&mut self, job: &UnprocessedJob) -> Result<(), UnprocessedJobsRepositoryError>;
    fn delete_unprocessed_job(&mut self, id: &str) -> Result<(), UnprocessedJobsRepositoryError>;
}
