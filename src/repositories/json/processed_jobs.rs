use super::{JsonUserDataRepository, UnresolvedProcessedJob};
use crate::models::ProcessedJob;
use crate::repositories::{ProcessedJobsRepository, ProcessedJobsRepositoryError};

impl ProcessedJobsRepository for JsonUserDataRepository {
    fn get_all_processed_jobs(&self) -> Result<Vec<ProcessedJob>, ProcessedJobsRepositoryError> {
        self.unresolved_processed_jobs
            .values()
            .into_iter()
            .map(|job| {
                if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                    Ok(ProcessedJob {
                        start_time: job.start_time,
                        end_time: job.end_time,
                        job_id: job.job_id.clone(),
                        cpu_profile: profile.clone(),
                        energy: job.energy,
                        emissions: job.emissions,
                        generation_mix: job.generation_mix.clone(),
                    })
                } else {
                    Err(ProcessedJobsRepositoryError::MissingCpuProfile(
                        job.cpu_profile_name.clone(),
                    ))
                }
            })
            .collect()
    }

    fn get_processed_job_by_id(
        &self,
        id: &str,
    ) -> Result<Option<ProcessedJob>, ProcessedJobsRepositoryError> {
        if let Some(job) = self.unresolved_processed_jobs.get(id) {
            if let Some(profile) = self.cpu_profiles.get(&job.cpu_profile_name) {
                Ok(Some(ProcessedJob {
                    start_time: job.start_time,
                    end_time: job.end_time,
                    job_id: job.job_id.clone(),
                    cpu_profile: profile.clone(),
                    energy: job.energy,
                    emissions: job.emissions,
                    generation_mix: job.generation_mix.clone(),
                }))
            } else {
                Err(ProcessedJobsRepositoryError::MissingCpuProfile(
                    job.cpu_profile_name.clone(),
                ))
            }
        } else {
            Ok(None)
        }
    }

    fn upsert_processed_job(
        &mut self,
        job: &ProcessedJob,
    ) -> Result<(), ProcessedJobsRepositoryError> {
        self.cpu_profiles
            .insert(job.cpu_profile.name.clone(), job.cpu_profile.clone());
        let unresolved_job = UnresolvedProcessedJob {
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
            start_time: job.start_time,
            end_time: job.end_time,
            energy: job.energy,
            emissions: job.emissions,
            generation_mix: job.generation_mix.clone(),
        };
        self.unresolved_processed_jobs
            .insert(job.job_id.clone(), unresolved_job);
        Ok(())
    }

    fn delete_processed_job(&mut self, id: &str) -> Result<(), ProcessedJobsRepositoryError> {
        self.unresolved_processed_jobs.remove(id);
        Ok(())
    }
}
