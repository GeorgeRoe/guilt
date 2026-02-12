use super::json_collection::{JsonCollection, JsonKey};
use super::last_written_version::{LastWrittenVersion, LastWrittenVersionReadError};
use super::paths;
use crate::json_io::JsonFileOperationError;
use crate::models::{CpuProfile, ProcessedJob, UnprocessedJob};
use crate::profile_resolution::{ProfileResolutionPolicy, ProfileResolutionPolicyFromFileError};
use crate::users::User;
use crate::version::Version;
use std::path::{Path, PathBuf};
use thiserror::Error;
use std::fs;

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

impl JsonKey for CpuProfile {
    fn json_key(&self) -> String {
        self.name.clone()
    }
}

impl JsonKey for UnprocessedJob {
    fn json_key(&self) -> String {
        self.job_id.clone()
    }
}

impl JsonKey for ProcessedJob {
    fn json_key(&self) -> String {
        self.job_id.clone()
    }
}

pub struct GuiltDirectoryManager {
    path: PathBuf,
    cpu_profiles: Option<JsonCollection<CpuProfile>>,
    processed_jobs: Option<JsonCollection<ProcessedJob>>,
    unprocessed_jobs: Option<JsonCollection<UnprocessedJob>>,
    profile_resolution_policy_script: Option<String>
}

impl GuiltDirectoryManager {
    pub fn read(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
            cpu_profiles: None,
            processed_jobs: None,
            unprocessed_jobs: None,
            profile_resolution_policy_script: None
        }
    }

    pub fn read_for_user(user: &User) -> Self {
        let path = paths::guilt_directory_for_user(user);
        Self::read(&path)
    }

    pub fn empty_for_user(user: &User) -> Self {
        Self {
            path: paths::guilt_directory_for_user(user),
            cpu_profiles: JsonCollection::empty().into(),
            processed_jobs: JsonCollection::empty().into(),
            unprocessed_jobs: JsonCollection::empty().into(),
            profile_resolution_policy_script: None
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
        if let Some(unprocessed_jobs) = &self.unprocessed_jobs {
            unprocessed_jobs.write(&self.unprocessed_jobs_path())?;
            self.update_last_written_version()?;
        }
        if let Some(processed_jobs) = &self.processed_jobs {
            processed_jobs.write(&self.processed_jobs_path())?;
            self.update_last_written_version()?;
        }
        if let Some(script) = &self.profile_resolution_policy_script {
            fs::write(self.get_profile_resolution_policy_path(), script)?;
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
        Ok(
            LastWrittenVersion::read(&self.get_last_written_version_path())?
                .get()
                .clone(),
        )
    }

    fn update_last_written_version(&self) -> std::io::Result<()> {
        LastWrittenVersion::new().write(&self.get_last_written_version_path())
    }

    // cpu profile related methods

    fn cpu_profiles_path(&self) -> PathBuf {
        self.path.join(paths::CPU_PROFILES_FILE)
    }

    fn load_cpu_profiles(&mut self) -> Result<(), JsonFileOperationError> {
        let cpu_profiles = JsonCollection::read(&self.cpu_profiles_path())?;
        self.cpu_profiles = Some(cpu_profiles);
        Ok(())
    }

    fn get_cpu_profiles(
        &mut self,
    ) -> Result<&mut JsonCollection<CpuProfile>, JsonFileOperationError> {
        if self.cpu_profiles.is_none() {
            self.load_cpu_profiles()?;
        }
        Ok(self.cpu_profiles.as_mut().unwrap())
    }

    pub fn get_cpu_profile(
        &mut self,
        name: &str,
    ) -> Result<Option<CpuProfile>, JsonFileOperationError> {
        let cpu_profiles = self.get_cpu_profiles()?;
        Ok(cpu_profiles.get(name))
    }

    pub fn upsert_cpu_profile(
        &mut self,
        profile: CpuProfile,
    ) -> Result<(), JsonFileOperationError> {
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
        let unprocessed_jobs = JsonCollection::read(&self.unprocessed_jobs_path())?;
        self.unprocessed_jobs = Some(unprocessed_jobs);
        Ok(())
    }

    fn get_unprocessed_jobs(
        &mut self,
    ) -> Result<&mut JsonCollection<UnprocessedJob>, JsonFileOperationError> {
        if self.unprocessed_jobs.is_none() {
            self.load_unprocessed_jobs()?;
        }
        Ok(self.unprocessed_jobs.as_mut().unwrap())
    }

    pub fn get_unprocessed_job(
        &mut self,
        job_id: &str,
    ) -> Result<Option<UnprocessedJob>, GetJobError> {
        Ok(self.get_unprocessed_jobs()?.get(job_id))
    }

    pub fn get_all_unprocessed_jobs(&mut self) -> Result<Vec<UnprocessedJob>, GetJobError> {
        Ok(self.get_unprocessed_jobs()?.all())
    }

    pub fn upsert_unprocessed_job(
        &mut self,
        job: UnprocessedJob,
    ) -> Result<(), JsonFileOperationError> {
        self.get_unprocessed_jobs()?.upsert(job);
        Ok(())
    }

    pub fn remove_unprocessed_job(&mut self, job_id: &str) -> Result<(), JsonFileOperationError> {
        self.get_unprocessed_jobs()?.remove(job_id);
        Ok(())
    }

    // processed job related methods

    fn processed_jobs_path(&self) -> PathBuf {
        self.path.join(paths::PROCESSED_JOBS_FILE)
    }

    fn load_processed_jobs(&mut self) -> Result<(), JsonFileOperationError> {
        let processed_jobs = JsonCollection::read(&self.processed_jobs_path())?;
        self.processed_jobs = Some(processed_jobs);
        Ok(())
    }

    fn get_processed_jobs(
        &mut self,
    ) -> Result<&mut JsonCollection<ProcessedJob>, JsonFileOperationError> {
        if self.processed_jobs.is_none() {
            self.load_processed_jobs()?;
        }
        Ok(self.processed_jobs.as_mut().unwrap())
    }

    pub fn get_processed_job(&mut self, job_id: &str) -> Result<Option<ProcessedJob>, GetJobError> {
        Ok(self.get_processed_jobs()?.get(job_id))
    }

    pub fn get_all_processed_jobs(&mut self) -> Result<Vec<ProcessedJob>, GetJobError> {
        Ok(self.get_processed_jobs()?.all())
    }

    pub fn upsert_processed_job(
        &mut self,
        job: ProcessedJob,
    ) -> Result<(), JsonFileOperationError> {
        self.get_processed_jobs()?.upsert(job);
        Ok(())
    }

    pub fn remove_processed_job(&mut self, job_id: &str) -> Result<(), JsonFileOperationError> {
        self.get_processed_jobs()?.remove(job_id);
        Ok(())
    }

    // profile resolution policy related methods

    fn get_profile_resolution_policy_path(&self) -> PathBuf {
        self.path.join(paths::PROFILE_RESOLUTION_POLICY_FILE)
    }

    pub fn get_profile_resolution_policy(
        &self,
    ) -> Result<ProfileResolutionPolicy, ProfileResolutionPolicyFromFileError> {
        ProfileResolutionPolicy::from_file(&self.get_profile_resolution_policy_path())
    }

    pub fn set_profile_resolution_policy_script(&mut self, script: String) {
        self.profile_resolution_policy_script = Some(script);
    }
}
