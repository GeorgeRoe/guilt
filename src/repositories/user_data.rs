use super::{CpuProfilesRepository, ProcessedJobsRepository, UnprocessedJobsRepository};
use crate::users::User;

pub trait UserDataRepository:
    CpuProfilesRepository + UnprocessedJobsRepository + ProcessedJobsRepository
{
    fn setup(user: &User) -> anyhow::Result<()>;
    fn new(user: &User) -> anyhow::Result<Self>
    where
        Self: Sized;
    fn commit(&self) -> anyhow::Result<()>;
}
