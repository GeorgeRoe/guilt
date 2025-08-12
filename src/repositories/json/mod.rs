pub mod io;
pub mod paths;

use crate::models::CpuProfile;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedUnprocessedJob {
    pub job_id: String,
    pub cpu_profile_name: String,
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
mod processed_jobs;
mod unprocessed_jobs;
mod user_data;
