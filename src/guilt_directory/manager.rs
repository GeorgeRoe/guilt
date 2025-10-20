use crate::models::{
    CpuProfile,
    ProcessedJob,
    UnprocessedJob,
};
use super::{
    CpuProfiles,
    UnresolvedProcessedJobs,
    UnresolvedUnprocessedJobs,
    paths,
    LastWrittenVersion,
    LastWrittenVersionReadError,
    UnresolvedProcessedJob,
    UnresolvedUnprocessedJob,
};
use std::path::{Path, PathBuf};
use crate::json_io::JsonFileOperationError;
use thiserror::Error;
use crate::users::User;
use crate::version::Version;

#[derive(Debug, Error)]
pub enum GuiltDirectorySetupError {
    #[error("I/O error: {0}")]
    IoError(#[from] std::io::Error),
    #[error("JSON file operation error: {0}")]
    JsonFileOperationError(#[from] JsonFileOperationError),
}

#[derive(Debug, Error)]
pub enum GetJobError {
    #[error("CPU profile with the name '{0}' was not found.")]
    CpuProfileNotFoundError(String),
    #[error("JSON file operation error: {0}")]
    JsonFileOperationError(#[from] JsonFileOperationError),
}

#[derive(Debug, Error)]
pub enum UpsertJobError {
    #[error("A CPU profile with the same name but different details already exists.")]
    CpuProfileAlreadyExistsError,
    #[error("JSON file operation error: {0}")]
    JsonFileOperationError(#[from] JsonFileOperationError),
}

pub struct GuiltDirectoryManager {
    path: PathBuf,
    cpu_profiles: Option<CpuProfiles>,
    unresolved_processed_jobs: Option<UnresolvedProcessedJobs>,
    unresolved_unprocessed_jobs: Option<UnresolvedUnprocessedJobs>,
}

impl GuiltDirectoryManager {
    pub fn read(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
            cpu_profiles: None,
            unresolved_processed_jobs: None,
            unresolved_unprocessed_jobs: None,
        }
    }

    pub fn read_for_user(user: &User) -> Self {
        let path = paths::guilt_directory_for_user(user);
        Self::read(&path)
    }

    pub fn empty_for_user(user: &User) -> Self {
        Self {
            path: paths::guilt_directory_for_user(user),
            cpu_profiles: CpuProfiles::empty().into(),
            unresolved_processed_jobs: UnresolvedProcessedJobs::empty().into(),
            unresolved_unprocessed_jobs: UnresolvedUnprocessedJobs::empty().into(),
        }
    }

    pub fn create_directory_for_user(user: &User) -> std::io::Result<()> {
        std::fs::create_dir(paths::guilt_directory_for_user(user))
    }

    pub fn setup_for_user(user: &User) -> Result<Self, GuiltDirectorySetupError> {
        Self::create_directory_for_user(user)?;

        let manager = Self::empty_for_user(user);
        manager.write()?;

        Ok(manager)
    }

    pub fn teardown(&self) -> std::io::Result<()> {
        std::fs::remove_dir_all(&self.path)
    }

    pub fn write(&self) -> Result<(), JsonFileOperationError> {
        if let Some(cpu_profiles) = &self.cpu_profiles {
            cpu_profiles.write(&self.cpu_profiles_path())?;
            self.update_last_written_version()?;
        }
        if let Some(unresolved_unprocessed_jobs) = &self.unresolved_unprocessed_jobs {
            unresolved_unprocessed_jobs.write(&self.unprocessed_jobs_path())?;
            self.update_last_written_version()?;
        }
        if let Some(unresolved_processed_jobs) = &self.unresolved_processed_jobs {
            unresolved_processed_jobs.write(&self.processed_jobs_path())?;
            self.update_last_written_version()?;
        }

        Ok(())
    }

    pub fn path(&self) -> &Path {
        &self.path
    }

    // last written version related methods

    fn get_last_written_version_path(&self) -> PathBuf {
        self.path.join(paths::LAST_WRITTEN_VERSION_FILE)
    }

    pub fn get_last_written_version(&mut self) -> Result<Version, LastWrittenVersionReadError> {
        Ok(LastWrittenVersion::read(&self.get_last_written_version_path())?.get().clone())
    }

    fn update_last_written_version(&self) -> std::io::Result<()> {
        LastWrittenVersion::new().write(&self.get_last_written_version_path())
    }

    // cpu profile related methods

    fn cpu_profiles_path(&self) -> PathBuf {
        self.path.join(paths::CPU_PROFILES_FILE)
    }

    fn load_cpu_profiles(&mut self) -> Result<(), JsonFileOperationError> {
        let cpu_profiles = CpuProfiles::read(&self.cpu_profiles_path())?;
        self.cpu_profiles = Some(cpu_profiles);
        Ok(())
    }

    fn get_cpu_profiles(&mut self) -> Result<&mut CpuProfiles, JsonFileOperationError> {
        if self.cpu_profiles.is_none() {
            self.load_cpu_profiles()?;
        }
        Ok(self.cpu_profiles.as_mut().unwrap())
    }

    pub fn get_cpu_profile(&mut self, name: &str) -> Result<Option<CpuProfile>, JsonFileOperationError> {
        let cpu_profiles = self.get_cpu_profiles()?;
        Ok(cpu_profiles.get(name))
    }

    pub fn upsert_cpu_profile(&mut self, profile: CpuProfile) -> Result<(), JsonFileOperationError> {
        let cpu_profiles = self.get_cpu_profiles()?;
        cpu_profiles.upsert(profile);
        Ok(())
    }

    pub fn remove_cpu_profile(&mut self, name: &str) -> Result<(), JsonFileOperationError> {
        let cpu_profiles = self.get_cpu_profiles()?;
        cpu_profiles.remove(name);
        Ok(())
    }

    // unprocessed job related methods

    fn unprocessed_jobs_path(&self) -> PathBuf {
        self.path.join(paths::UNPROCESSED_JOBS_FILE)
    }

    fn load_unprocessed_jobs(&mut self) -> Result<(), JsonFileOperationError> {
        let unresolved_unprocessed_jobs = UnresolvedUnprocessedJobs::read(&self.unprocessed_jobs_path())?;
        self.unresolved_unprocessed_jobs = Some(unresolved_unprocessed_jobs);
        Ok(())
    }

    fn get_unresolved_unprocessed_jobs(&mut self) -> Result<&mut UnresolvedUnprocessedJobs, JsonFileOperationError> {
        if self.unresolved_unprocessed_jobs.is_none() {
            self.load_unprocessed_jobs()?;
        }
        Ok(self.unresolved_unprocessed_jobs.as_mut().unwrap())
    }

    pub fn get_unprocessed_job(&mut self, job_id: &str) -> Result<Option<UnprocessedJob>, GetJobError> {
        if let Some(unresolved_job) = self.get_unresolved_unprocessed_jobs()?.get(job_id) {
            if let Some(cpu_profile) = self.get_cpu_profile(&unresolved_job.cpu_profile_name)? {
                Ok(Some(unresolved_job.resolve(&cpu_profile)))
            } else {
               Err(GetJobError::CpuProfileNotFoundError(unresolved_job.cpu_profile_name.clone())) 
            }
        } else {
            Ok(None)
        }
    }

    pub fn get_all_unprocessed_jobs(&mut self) -> Result<Vec<UnprocessedJob>, GetJobError> {
        let unresolved_jobs = self.get_unresolved_unprocessed_jobs()?.all();
        unresolved_jobs.into_iter().map(|job| {
            if let Some(cpu_profile) = self.get_cpu_profile(&job.cpu_profile_name)? {
                Ok(job.resolve(&cpu_profile))
            } else {
                Err(GetJobError::CpuProfileNotFoundError(job.cpu_profile_name.clone()))
            }
        }).collect()
    }

    pub fn upsert_unprocessed_job(&mut self, job: UnprocessedJob) -> Result<(), UpsertJobError> {
        if let Some(existing_profile) = self.get_cpu_profile(&job.cpu_profile.name)? && existing_profile != job.cpu_profile {
            Err(UpsertJobError::CpuProfileAlreadyExistsError)
        } else {
            let unresolved_job = UnresolvedUnprocessedJob::unresolve(&job);
            self.get_unresolved_unprocessed_jobs()?.upsert(unresolved_job);
            self.upsert_cpu_profile(job.cpu_profile)?;
            Ok(())
        }
    }

    pub fn remove_unprocessed_job(&mut self, job_id: &str) -> Result<(), JsonFileOperationError> {
        self.get_unresolved_unprocessed_jobs()?.remove(job_id);
        Ok(())
    }

    // processed job related methods

    fn processed_jobs_path(&self) -> PathBuf {
        self.path.join(paths::PROCESSED_JOBS_FILE)
    }

    fn load_processed_jobs(&mut self) -> Result<(), JsonFileOperationError> {
        let unresolved_processed_jobs = UnresolvedProcessedJobs::read(&self.processed_jobs_path())?;
        self.unresolved_processed_jobs = Some(unresolved_processed_jobs);
        Ok(())
    }

    fn get_processed_jobs(&mut self) -> Result<&mut UnresolvedProcessedJobs, JsonFileOperationError> {
        if self.unresolved_processed_jobs.is_none() {
            self.load_processed_jobs()?;
        }
        Ok(self.unresolved_processed_jobs.as_mut().unwrap())
    }

    pub fn get_all_processed_jobs(&mut self) -> Result<Vec<ProcessedJob>, GetJobError> {
        let unresolved_jobs = self.get_processed_jobs()?.all();
        unresolved_jobs.into_iter().map(|job| {
            if let Some(cpu_profile) = self.get_cpu_profile(&job.cpu_profile_name)? {
                Ok(job.resolve(&cpu_profile))
            } else {
                Err(GetJobError::CpuProfileNotFoundError(job.cpu_profile_name.clone()))
            }
        }).collect()
    }

    pub fn get_processed_job(&mut self, job_id: &str) -> Result<Option<ProcessedJob>, GetJobError> {
        if let Some(unresolved_job) = self.get_processed_jobs()?.get(job_id) {
            if let Some(cpu_profile) = self.get_cpu_profile(&unresolved_job.cpu_profile_name)? {
                Ok(Some(unresolved_job.resolve(&cpu_profile)))
            } else {
                Err(GetJobError::CpuProfileNotFoundError(unresolved_job.cpu_profile_name.clone()))
            }
        } else {
            Ok(None)
        }
    }

    pub fn upsert_processed_job(&mut self, job: ProcessedJob) -> Result<(), UpsertJobError> {
        if let Some(existing_profile) = self.get_cpu_profile(&job.cpu_profile.name)? && existing_profile != job.cpu_profile {
            Err(UpsertJobError::CpuProfileAlreadyExistsError)
        } else {
            let unresolved_job = UnresolvedProcessedJob::unresolve(&job);
            self.get_processed_jobs()?.upsert(unresolved_job);
            self.upsert_cpu_profile(job.cpu_profile)?;
            Ok(())
        }
    }

    pub fn remove_processed_job(&mut self, job_id: &str) -> Result<(), JsonFileOperationError> {
        self.get_processed_jobs()?.remove(job_id);
        Ok(())
    }
}