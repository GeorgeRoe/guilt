use chrono::{DateTime, Utc};

pub struct SlurmBatchTest {
    pub job_id: String,
    pub start_time: DateTime<Utc>,
    pub processor_count: i32,
    pub nodes: String,
    pub partition: String,
}
