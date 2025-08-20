use chrono::{DateTime, Utc};
use std::collections::HashMap;

pub struct CarbonIntensityTimeSegment {
    pub from: DateTime<Utc>,
    pub to: DateTime<Utc>,
    pub intensity: i32,
    pub generation_mix: HashMap<String, f64>,
}
