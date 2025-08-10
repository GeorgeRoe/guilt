use crate::models::UnprocessedJob;
use std::result::Result;
use crate::SomeError;

pub trait UnprocessedJobsRepository {
    fn get_all_jobs(&self) -> Result<Vec<UnprocessedJob>, SomeError>;
    fn get_job_by_id(&self, id: &str) -> Result<Option<UnprocessedJob>, SomeError>;
    fn upsert_job(&mut self, job: &UnprocessedJob) -> Result<(), SomeError>;
    fn delete_job(&mut self, id: &str) -> Result<(), SomeError>;
    fn commit(&self) -> Result<(), SomeError>;
}