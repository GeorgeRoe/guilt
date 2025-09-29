use super::JsonUserDataRepository;
use super::paths::{
    cpu_profiles_file_given_guilt_dir, processed_jobs_file_given_guilt_dir,
    unprocessed_jobs_file_given_guilt_dir, user_data_dir_given_guilt_dir,
};
use super::{UnresolvedProcessedJob, UnresolvedUnprocessedJob};
use crate::guilt_dir::guilt_dir_given_home;
use crate::models::CpuProfile;
use crate::repositories::UserDataRepository;
use crate::users::User;
use crate::json_io::{read_json_file, write_json_file};
use std::fs;

impl UserDataRepository for JsonUserDataRepository {
    fn setup(user: &User) -> anyhow::Result<()> {
        let guilt_dir = guilt_dir_given_home(&user.home_dir);
        fs::create_dir_all(user_data_dir_given_guilt_dir(&guilt_dir))?;

        let empty: Vec<serde_json::Value> = Vec::new();

        write_json_file(cpu_profiles_file_given_guilt_dir(&guilt_dir), &empty)?;
        write_json_file(unprocessed_jobs_file_given_guilt_dir(&guilt_dir), &empty)?;
        write_json_file(processed_jobs_file_given_guilt_dir(&guilt_dir), &empty)?;

        Ok(())
    }

    fn new(user: &User) -> anyhow::Result<Self> {
        let guilt_dir = guilt_dir_given_home(&user.home_dir);

        let cpu_profiles: Vec<CpuProfile> =
            read_json_file(cpu_profiles_file_given_guilt_dir(&guilt_dir))?;
        let unresolved_unprocessed_jobs: Vec<UnresolvedUnprocessedJob> =
            read_json_file(unprocessed_jobs_file_given_guilt_dir(&guilt_dir))?;
        let unresolved_processed_jobs: Vec<UnresolvedProcessedJob> =
            read_json_file(processed_jobs_file_given_guilt_dir(&guilt_dir))?;

        Ok(JsonUserDataRepository {
            path: guilt_dir,
            cpu_profiles: cpu_profiles
                .into_iter()
                .map(|profile| (profile.name.clone(), profile))
                .collect(),
            unresolved_unprocessed_jobs: unresolved_unprocessed_jobs
                .into_iter()
                .map(|job| (job.job_id.clone(), job))
                .collect(),
            unresolved_processed_jobs: unresolved_processed_jobs
                .into_iter()
                .map(|job| (job.job_id.clone(), job))
                .collect(),
        })
    }

    fn commit(&self) -> anyhow::Result<()> {
        write_json_file(
            cpu_profiles_file_given_guilt_dir(&self.path),
            &self.cpu_profiles.values().collect::<Vec<&CpuProfile>>(),
        )?;
        write_json_file(
            unprocessed_jobs_file_given_guilt_dir(&self.path),
            &self
                .unresolved_unprocessed_jobs
                .values()
                .collect::<Vec<&UnresolvedUnprocessedJob>>(),
        )?;
        write_json_file(
            processed_jobs_file_given_guilt_dir(&self.path),
            &self
                .unresolved_processed_jobs
                .values()
                .collect::<Vec<&UnresolvedProcessedJob>>(),
        )?;

        Ok(())
    }
}
