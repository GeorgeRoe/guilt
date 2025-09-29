pub mod io;
pub mod paths;

mod unresolved_unprocessed_job;
pub use unresolved_unprocessed_job::UnresolvedUnprocessedJob;

mod unresolved_processed_job;
pub use unresolved_processed_job::UnresolvedProcessedJob;

mod cpu_profiles;
mod processed_jobs;
mod unprocessed_jobs;
mod user_data;

use crate::models::CpuProfile;
use std::path::PathBuf;
use std::collections::HashMap;

pub struct JsonUserDataRepository {
    path: PathBuf,

    cpu_profiles: HashMap<String, CpuProfile>,
    unresolved_unprocessed_jobs: HashMap<String, UnresolvedUnprocessedJob>,
    unresolved_processed_jobs: HashMap<String, UnresolvedProcessedJob>,
}
