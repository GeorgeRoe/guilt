use crate::{repositories::UserDataRepository};
use crate::users::User;
use std::collections::HashMap;
use std::result::Result;
use crate::SomeError;
use crate::guilt_dir::guilt_dir_given_home;
use super::JsonUserDataRepository;

impl UserDataRepository for JsonUserDataRepository {
    fn new(user: User) -> Result<Self, SomeError> {
        Ok(JsonUserDataRepository {
            path: guilt_dir_given_home(&user.home_dir),
            cpu_profiles: HashMap::new(),
            unresolved_unprocessed_jobs: HashMap::new(),
        })
    }

    fn commit(&self) -> Result<(), SomeError> {
        Ok(())
    }
}