use super::unresolved_unprocessed_jobs::JsonUnresolvedUnprocessedJobsRepository;
use super::unresolved_unprocessed_jobs::UnresolvedUnprocessedJob;
use super::JsonCpuProfilesRepository;
use crate::repositories::CpuProfilesRepository;
use crate::repositories::UnprocessedJobsRepository;
use crate::models::UnprocessedJob;
use crate::SomeError;

#[derive(Debug)]
pub enum JsonUnprocessedJobsRepositoryError {
    CpuProfileNotFound(String)
}

impl std::fmt::Display for JsonUnprocessedJobsRepositoryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            JsonUnprocessedJobsRepositoryError::CpuProfileNotFound(name) => write!(f, "CPU profile '{}' not found", name)
        }
    }
}

impl std::error::Error for JsonUnprocessedJobsRepositoryError {}

pub struct JsonUnprocessedJobsRepository {
    unresolved_unprocessed_jobs_repository: JsonUnresolvedUnprocessedJobsRepository,
    cpu_profiles_repository: JsonCpuProfilesRepository
}

impl JsonUnprocessedJobsRepository {
    pub fn new(
        unresolved_unprocessed_jobs_repository: JsonUnresolvedUnprocessedJobsRepository,
        cpu_profiles_repository: JsonCpuProfilesRepository
    ) -> Self {
        JsonUnprocessedJobsRepository {
            unresolved_unprocessed_jobs_repository,
            cpu_profiles_repository
        }
    }

    fn resolve_job(&self, job: &UnresolvedUnprocessedJob) -> Result<UnprocessedJob, SomeError> {
        if let Some(profile) = self.cpu_profiles_repository.get_profile_by_name(&job.cpu_profile_name)? {
            Ok(UnprocessedJob {
                job_id: job.job_id.clone(),
                cpu_profile: profile
            })
        } else {
            Err(JsonUnprocessedJobsRepositoryError::CpuProfileNotFound(job.cpu_profile_name.clone()).into())
        }
    }
}

impl UnprocessedJobsRepository for JsonUnprocessedJobsRepository {
    fn get_all_jobs(&self) -> Result<Vec<UnprocessedJob>, SomeError> {
        Ok(self.unresolved_unprocessed_jobs_repository.get_all_jobs()
            .into_iter()
            .map(|job| self.resolve_job(&job))
            .collect::<Result<Vec<_>, _>>()?
        )
    }

    fn get_job_by_id(&self, job_id: &str) -> Result<Option<UnprocessedJob>, SomeError> {
        if let Some(job) = self.unresolved_unprocessed_jobs_repository.get_job_by_id(job_id) {
            Ok(Some(self.resolve_job(&job)?))
        } else {
            Ok(None)
        }
    }

    fn upsert_job(&mut self, job: &UnprocessedJob) -> Result<(), SomeError> {
        self.cpu_profiles_repository.upsert_profile(&job.cpu_profile)?;
        let unresolved_job = UnresolvedUnprocessedJob {
            job_id: job.job_id.clone(),
            cpu_profile_name: job.cpu_profile.name.clone(),
        };
        self.unresolved_unprocessed_jobs_repository.upsert_job(&unresolved_job);
        Ok(())
    }

    fn delete_job(&mut self, job_id: &str) -> Result<(), SomeError> {
        self.unresolved_unprocessed_jobs_repository.delete_job(job_id);
        Ok(())
    }

    fn commit(&self) -> Result<(), SomeError> {
        self.unresolved_unprocessed_jobs_repository.commit()?;
        self.cpu_profiles_repository.commit()?;
        Ok(())
    }
}