pub mod io;
pub mod paths;

use std::path::PathBuf;
use std::collections::HashMap;
use crate::models::CpuProfile;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedUnprocessedJob {
    pub job_id: String,
    pub cpu_profile_name: String
}

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedProcessedJob {
    pub start_time: DateTime<Utc>,
    pub end_time: DateTime<Utc>,
    pub job_id: String,
    pub cpu_profile_name: String,
    pub energy: f64,
    pub emissions: f64,
    pub generation_mix: HashMap<String, f64>,
}

pub struct JsonUserDataRepository {
    path: PathBuf,

    cpu_profiles: HashMap<String, CpuProfile>,
    unresolved_unprocessed_jobs: HashMap<String, UnresolvedUnprocessedJob>,
    unresolved_processed_jobs: HashMap<String, UnresolvedProcessedJob>,
}

mod cpu_profiles;
mod unprocessed_jobs;
mod processed_jobs;
mod user_data;