use std::path::PathBuf;
use std::collections::HashMap;
use crate::models::CpuProfile;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedUnprocessedJob {
    pub job_id: String,
    pub cpu_profile_name: String
}

pub struct JsonUserDataRepository {
    path: PathBuf,

    cpu_profiles: HashMap<String, CpuProfile>,
    unresolved_unprocessed_jobs: HashMap<String, UnresolvedUnprocessedJob>
}

impl JsonUserDataRepository {
}

mod cpu_profiles;
mod unprocessed_jobs;
mod user_data;