use crate::SomeError;
use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{UserDataRepository, CpuProfilesRepository, UnprocessedJobsRepository, ProcessedJobsRepository};
use crate::users::get_current_user;

pub fn run() -> Result<(), SomeError> {
    println!("NOT IMPLEMENTED");

    let user_data_repo = JsonUserDataRepository::new(get_current_user()?)?;

    println!("{}", user_data_repo.get_all_cpu_profiles()?.len());
    println!("{}", user_data_repo.get_all_unprocessed_jobs()?.len());
    println!("{}", user_data_repo.get_all_processed_jobs()?.len());

    Ok(())
}