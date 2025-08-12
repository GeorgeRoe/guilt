use super::{JsonUserDataRepository, UnresolvedUnprocessedJob};
use crate::SomeError;
use crate::models::UnprocessedJob;
use crate::repositories::UnprocessedJobsRepository;

impl UnprocessedJobsRepository for JsonUserDataRepository {
    fn get_all_unprocessed_jobs(&self) -> Result<Vec<UnprocessedJob>, SomeError> {
        self.unresolved_unprocessed_jobs
            .values()
            .into_iter()
            .map(|job| {
                if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                    Ok(UnprocessedJob {
                        job_id: job.job_id.clone(),
                        cpu_profile: profile.clone(),
                    })
                } else {
                    Err(Box::<dyn std::error::Error>::from(std::io::Error::new(
                        std::io::ErrorKind::NotFound,
                        format!("CPU profile '{}' not found", job.cpu_profile_name),
                    )))
                }
            })
            .collect()
    }

    fn get_unprocessed_job_by_id(&self, job_id: &str) -> Result<Option<UnprocessedJob>, SomeError> {
        if let Some(job) = self.unresolved_unprocessed_jobs.get(job_id) {
            if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                Ok(Some(UnprocessedJob {
                    job_id: job.job_id.clone(),
                    cpu_profile: profile.clone(),
                }))
            } else {
                Err(Box::<dyn std::error::Error>::from(std::io::Error::new(
                    std::io::ErrorKind::NotFound,
                    format!("CPU profile '{}' not found", job.cpu_profile_name),
                )))
            }
        } else {
            Ok(None)
        }
    }

    fn upsert_unprocessed_job(&mut self, job: &UnprocessedJob) -> Result<(), SomeError> {
        self.cpu_profiles
            .insert(job.cpu_profile.name.clone(), job.cpu_profile.clone());
        let unresolved_job = UnresolvedUnprocessedJob {
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
        };
        self.unresolved_unprocessed_jobs
            .insert(job.job_id.clone(), unresolved_job);
        Ok(())
    }

    fn delete_unprocessed_job(&mut self, id: &str) -> Result<(), SomeError> {
        self.unresolved_unprocessed_jobs.remove(id);
        Ok(())
    }
}
