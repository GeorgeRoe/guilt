use super::CpuProfilesRepository;
use super::UnprocessedJobsRepository;
use crate::users::User;
use std::result::Result;
use crate::SomeError;

pub trait UserDataRepository: CpuProfilesRepository + UnprocessedJobsRepository {
    fn new(user: User) -> Result<Self, SomeError> where Self: Sized;
    fn commit(&self) -> Result<(), SomeError>;
}