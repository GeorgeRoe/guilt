use super::{CpuProfilesRepository, UnprocessedJobsRepository, ProcessedJobsRepository};
use crate::users::User;
use std::result::Result;
use crate::SomeError;

pub trait UserDataRepository: CpuProfilesRepository + UnprocessedJobsRepository + ProcessedJobsRepository {
    fn setup(user: User) -> Result<(), SomeError>;
    fn new(user: User) -> Result<Self, SomeError> where Self: Sized;
    fn commit(&self) -> Result<(), SomeError>;
}