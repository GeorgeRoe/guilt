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
    LastWrittenVersionReadError
};
use std::path::{Path, PathBuf};
use crate::json_io::JsonFileOperationError;

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

    // last written version related methods

    fn get_last_written_version_path(&self) -> PathBuf {
        self.path.join(paths::LAST_WRITTEN_VERSION_FILE)
    }

    fn get_last_written_version(&mut self) -> Result<LastWrittenVersion, LastWrittenVersionReadError> {
        LastWrittenVersion::read(&self.get_last_written_version_path())
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

    // unprocessed job related methods

    fn unprocessed_jobs_path(&self) -> PathBuf {
        self.path.join(paths::UNPROCESSED_JOBS_FILE)
    }

    fn load_unprocessed_jobs(&mut self) -> Result<(), JsonFileOperationError> {
        let unresolved_unprocessed_jobs = UnresolvedUnprocessedJobs::read(&self.unprocessed_jobs_path())?;
        self.unresolved_unprocessed_jobs = Some(unresolved_unprocessed_jobs);
        Ok(())
    }

    fn get_unprocessed_jobs(&mut self) -> Result<&mut UnresolvedUnprocessedJobs, JsonFileOperationError> {
        if self.unresolved_unprocessed_jobs.is_none() {
            self.load_unprocessed_jobs()?;
        }
        Ok(self.unresolved_unprocessed_jobs.as_mut().unwrap())
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
}