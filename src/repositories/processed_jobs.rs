use crate::models::ProcessedJob;
use std::result::Result;
use crate::SomeError;

pub trait ProcessedJobsRepository {
    fn get_all_processed_jobs(&self) -> Result<Vec<ProcessedJob>, SomeError>;
    fn get_processed_job_by_id(&self, id: &str) -> Result<Option<ProcessedJob>, SomeError>;
    fn upsert_processed_job(&mut self, job: &ProcessedJob) -> Result<(), SomeError>;
    fn delete_processed_job(&mut self, id: &str) -> Result<(), SomeError>;
}