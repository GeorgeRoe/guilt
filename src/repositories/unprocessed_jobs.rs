use crate::models::UnprocessedJob;
use std::result::Result;
use crate::SomeError;

pub trait UnprocessedJobsRepository {
    fn get_all_unprocessed_jobs(&self) -> Result<Vec<UnprocessedJob>, SomeError>;
    fn get_unprocessed_job_by_id(&self, id: &str) -> Result<Option<UnprocessedJob>, SomeError>;
    fn upsert_unprocessed_job(&mut self, job: &UnprocessedJob) -> Result<(), SomeError>;
    fn delete_unprocessed_job(&mut self, id: &str) -> Result<(), SomeError>;
}