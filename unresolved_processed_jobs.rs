use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::result::Result;
use crate::SomeError;
use std::collections::HashMap;
use chrono::{DateTime, Utc};

#[derive(Serialize, Deserialize, Clone)]
pub struct UnresolvedProcessedJob {
    start_time: DateTime<Utc>,
    end_time: DateTime<Utc>,
    job_id: String,
    cpu_profile_name: String,
    energy: f64,
    emissions: f64,
    generation_mix: HashMap<String, f64>
}