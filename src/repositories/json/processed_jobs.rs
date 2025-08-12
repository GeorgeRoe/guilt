use super::{JsonUserDataRepository, UnresolvedProcessedJob};
use crate::repositories::ProcessedJobsRepository;
use crate::models::ProcessedJob;
use crate::SomeError;

impl ProcessedJobsRepository for JsonUserDataRepository {
    fn get_all_processed_jobs(&self) -> Result<Vec<ProcessedJob>, SomeError> {
        self.unresolved_processed_jobs.values()
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
                    Err(Box::<dyn std::error::Error>::from(std::io::Error::new(
                        std::io::ErrorKind::NotFound,
                        format!("Cpu profile '{}' not found", job.cpu_profile_name)
                    )))
                }
            })
            .collect()
    }

    fn get_processed_job_by_id(&self, id: &str) -> Result<Option<ProcessedJob>, SomeError> {
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
                Err(Box::<dyn std::error::Error>::from(std::io::Error::new(
                    std::io::ErrorKind::NotFound,
                    format!("CPU profile '{}' not found", job.cpu_profile_name)
                )))
            }
        } else {
            Ok(None)
        }
    }

    fn upsert_processed_job(&mut self, job: &ProcessedJob) -> Result<(), SomeError> {
        self.cpu_profiles.insert(job.cpu_profile.name.clone(), job.cpu_profile.clone());
        let unresolved_job = UnresolvedProcessedJob {
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
            start_time: job.start_time,
            end_time: job.end_time,
            energy: job.energy,
            emissions: job.emissions,
            generation_mix: job.generation_mix.clone(),
        };
        self.unresolved_processed_jobs.insert(job.job_id.clone(), unresolved_job);
        Ok(())
    }

    fn delete_processed_job(&mut self, id: &str) -> Result<(), SomeError> {
        self.unresolved_processed_jobs.remove(id);
        Ok(())
    }
}