use crate::{repositories::UserDataRepository};
use crate::users::User;
use std::result::Result;
use crate::SomeError;
use crate::guilt_dir::guilt_dir_given_home;
use super::JsonUserDataRepository;
use super::io::{CPU_PROFILES_FILE, UNPROCESSED_JOBS_FILE, read_json_file, write_json_file};
use crate::models::CpuProfile;
use super::UnresolvedUnprocessedJob;

impl UserDataRepository for JsonUserDataRepository {
    fn new(user: User) -> Result<Self, SomeError> {
        let guilt_dir = guilt_dir_given_home(&user.home_dir);

        let cpu_profiles: Vec<CpuProfile> = read_json_file(guilt_dir.join(CPU_PROFILES_FILE))?;
        let unresolved_unprocessed_jobs: Vec<UnresolvedUnprocessedJob> = read_json_file(guilt_dir.join(UNPROCESSED_JOBS_FILE))?;

        Ok(JsonUserDataRepository {
            path: guilt_dir,
            cpu_profiles: cpu_profiles.into_iter()
                .map(|profile| (profile.name.clone(), profile))
                .collect(),
            unresolved_unprocessed_jobs: unresolved_unprocessed_jobs.into_iter()
                .map(|job| (job.job_id.clone(), job))
                .collect(),
        })
    }

    fn commit(&self) -> Result<(), SomeError> {
        write_json_file(self.path.join(CPU_PROFILES_FILE), &self.cpu_profiles.values().collect::<Vec<&CpuProfile>>())?;
        write_json_file(self.path.join(UNPROCESSED_JOBS_FILE), &self.unresolved_unprocessed_jobs.values().collect::<Vec<&UnresolvedUnprocessedJob>>())?;

        Ok(())
    }
}