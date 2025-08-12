use super::CpuProfile;
use chrono::{DateTime, Utc};
use std::collections::HashMap;

pub struct ProcessedJob {
    pub start_time: DateTime<Utc>,
    pub end_time: DateTime<Utc>,
    pub job_id: String,
    pub cpu_profile: CpuProfile,
    pub energy: f64,
    pub emissions: f64,
    pub generation_mix: HashMap<String, f64>,
}
