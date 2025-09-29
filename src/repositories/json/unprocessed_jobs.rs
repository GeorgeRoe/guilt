use super::{JsonUserDataRepository, UnresolvedUnprocessedJob};
use crate::models::UnprocessedJob;
use crate::repositories::{UnprocessedJobsRepository, UnprocessedJobsRepositoryError};

impl UnprocessedJobsRepository for JsonUserDataRepository {
    fn get_all_unprocessed_jobs(
        &self,
    ) -> Result<Vec<UnprocessedJob>, UnprocessedJobsRepositoryError> {
        self.unresolved_unprocessed_jobs
            .values()
            .map(|job| {
                if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                    Ok(job.resolve(profile))
                } else {
                    Err(UnprocessedJobsRepositoryError::MissingCpuProfile(
                        job.cpu_profile_name.clone(),
                    ))
                }
            })
            .collect()
    }

    fn get_unprocessed_job_by_id(
        &self,
        job_id: &str,
    ) -> Result<Option<UnprocessedJob>, UnprocessedJobsRepositoryError> {
        if let Some(job) = self.unresolved_unprocessed_jobs.get(job_id) {
            if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                Ok(Some(job.resolve(profile)))
            } else {
                Err(UnprocessedJobsRepositoryError::MissingCpuProfile(
                    job.cpu_profile_name.clone(),
                ))
            }
        } else {
            Ok(None)
        }
    }

    fn upsert_unprocessed_job(
        &mut self,
        job: &UnprocessedJob,
    ) -> Result<(), UnprocessedJobsRepositoryError> {
        self.cpu_profiles
            .insert(job.cpu_profile.name.clone(), job.cpu_profile.clone());
        let unresolved_job = UnresolvedUnprocessedJob::unresolve(job);
        self.unresolved_unprocessed_jobs
            .insert(job.job_id.clone(), unresolved_job);
        Ok(())
    }

    fn delete_unprocessed_job(&mut self, id: &str) -> Result<(), UnprocessedJobsRepositoryError> {
        self.unresolved_unprocessed_jobs.remove(id);
        Ok(())
    }
}
